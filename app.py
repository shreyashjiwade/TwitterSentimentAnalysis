from flask import Flask, render_template, request, jsonify
from sentiment import get_tweet_sentiment
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    tweet_url = request.json.get("url", "")
    try:
        sentiment, text = get_tweet_sentiment(tweet_url)
        return jsonify({
            "sentiment": sentiment,
            "text": text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
