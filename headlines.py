from flask import Flask
import feedparser

BBC_FEED = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
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
	feed = feedparser.parse(BBC_FEED[publication])
	first_article = feed['entries'][0]
	return """<html>
		<body>
			<h1>BBC Headlines </h1>
			<b>{0}</b><br/>
			<b>{1}</b><br/>
			<b>{2}</b><br/>
		</body>
	</html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))

if __name__ == "__main__":
	app.run()