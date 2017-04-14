from flask import Flask
import feedparser

BBC_feed = 'http://feeds.bbci.co.uk/news/rss.xml'

app = Flask(__name__)

@app.route('/')
def get_news():
	feed = feedparser.parse(BBC_feed)
	first_article = feed['enteries'][0]
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