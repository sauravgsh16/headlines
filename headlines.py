from flask import Flask

app = Flask(__name__)

@app.route('/')
def get_news():
	return "these is no news"

if __name__ == "__main__":
	app.run()