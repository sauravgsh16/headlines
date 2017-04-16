import datetime
from flask import Flask, render_template, request
from flask import make_response
import feedparser
import json
import urllib2
import urllib


RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
			'cnn': 'http://rss.cnn.com/rss/edition.rss',
			'fox': 'http://feeds.foxnews.com/foxnews/latest'}

DEFAULTS = {"publication": "bbc",
			"city": "shillong",
			"currency_from": "GBP",
			"currency_to": "USD"}

app = Flask(__name__)
"""
@app.route('/')
@app.route('/bbc')
def bbc():
	return get_news('bbc')

@app.route('/cnn')
def cnn():
	return get_news('cnn')

@app.route('/fox')
def fox():
	return get_news('cnn')

def get_news(publication=None):
	feed = feedparser.parse(RSS_FEED[publication])
	return render_template('home.html', articles = feed['entries'])
"""

@app.route('/')
def home():
	# customized publication based on user input
	"""
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	"""
	publication = get_value_with_fallback("publication")
	articles = get_news(publication)

	#customized city based on user input or default
	city = get_value_with_fallback("city")
	weather = get_weather(city)

	#customized rate based on user input or default
	currency_from = get_value_with_fallback("currency_from")
	currency_to = get_value_with_fallback("currency_to")
	rates, currencies = get_rates(currency_from, currency_to)

	response = make_response(render_template('home.html', articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to,\
		rates=rates, currencies=sorted(currencies)))
	expires = datetime.datetime.now() + datetime.timedelta(days=365)
	
	#Setting cookies on response
	response.set_cookie("publication", publication, expires=expires)
	response.set_cookie("city", city, expires=expires)
	response.set_cookie("currency_from", currency_from, expires=expires)
	response.set_cookie("currency_to", currency_to, expires=expires)
	return response


def get_value_with_fallback(key):
	if request.args.get(key):
		return request.args.get(key)
	if request.cookies.get(key):
		return request.cookies.get(key)
	return DEFAULTS[key]

def get_news(query):
	if not query or query.lower() not in RSS_FEED:
		publication = DEFAULTS['publication']
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEED[publication])
	return feed['entries']

def get_weather(query):
	api_url = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid=79d26c3a9607e4f57f2161ff641fa697"
	query = urllib.quote(query)
	url = api_url.format(query)
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	if parsed.get("weather"):
		weather = {"description": parsed["weather"][0]["description"],
				"temperature": parsed["main"]["temp"],
				"city": parsed["name"],
				"country": parsed["sys"]["country"]}
	return weather

def get_rates(frm, to):
	api_url = "https://openexchangerates.org//api/latest.json?app_id=ac7bb4421eb549b89ebe2ca7046103f3"
	all_currency = urllib2.urlopen(api_url).read()

	parsed = json.loads(all_currency).get('rates')
	frm_rate = parsed.get(frm.upper())
	to_rate = parsed.get(to.upper())
	return (to_rate/frm_rate, parsed.keys())

if __name__ == "__main__":
	app.run()