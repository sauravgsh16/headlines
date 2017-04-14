from flask import Flask, render_template
import feedparser

RSS_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
			'cnn': 'http://rss.cnn.com/rss/edition.rss',
			'fox': 'http://feeds.foxnews.com/foxnews/latest'}


app = Flask(__name__)

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
	print publication
	feed = feedparser.parse(RSS_FEED[publication])
	first_article = feed['entries'][0]
	return render_template('home.html', title = first_article.get("title"), published = first_article.get("published"), summary = first_article.get("summary"))

if __name__ == "__main__":
	app.run()