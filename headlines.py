from flask import Flask, render_template, request
import feedparser
import json
import urllib2
import urllib


RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
			'cnn': 'http://rss.cnn.com/rss/edition.rss',
			'fox': 'http://feeds.foxnews.com/foxnews/latest'}

DEFAULTS = {"publication": "bbc",
			"city": "shillong"}

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
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	articles = get_news(publication)

	#customized city based on user input
	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)
	return render_template('home.html', articles=articles, weather=weather)

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

if __name__ == "__main__":
	app.run()