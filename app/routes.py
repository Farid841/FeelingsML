from flask import request, jsonify
from textblob import TextBlob
from . import app, db
from .models import Tweet

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    tweets = data.get('tweets', [])

    if not tweets:
        return jsonify({"error": "No tweets provided"}), 400

    sentiment_scores = {}

    for tweet in tweets:
        analysis = TextBlob(tweet)
        sentiment_scores[tweet] = analysis.sentiment.polarity

        positive = 1 if analysis.sentiment.polarity > 0 else 0
        negative = 1 if analysis.sentiment.polarity < 0 else 0

        new_tweet = Tweet(text=tweet, positive=positive, negative=negative)
        db.session.add(new_tweet)

    db.session.commit()

    return jsonify(sentiment_scores)