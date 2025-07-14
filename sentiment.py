import os
import re
import nltk
import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv

load_dotenv()
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
client = tweepy.Client(bearer_token=bearer_token)

def get_tweet_sentiment(tweet_url):
    # Extract tweet ID using regex
    match = re.search(r"status/(\d+)", tweet_url)
    if not match:
        raise ValueError("Invalid Tweet URL")
    tweet_id = match.group(1)

    tweet = client.get_tweet(id=tweet_id)
    if tweet.data is None:
        raise ValueError("Tweet not found or access denied")

    text = tweet.data["text"]
    score = sid.polarity_scores(text)
    
    if score['compound'] > 0.05:
        sentiment = "Positive"
    elif score['compound'] < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, text
