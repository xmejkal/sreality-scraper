from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Hello world</h1>"


@app.route("/scrape")
def scrape():

    return "Scraping"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5115, debug=True)
