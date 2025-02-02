from flask import request, jsonify
from flask_restx import Api, Resource, fields
from textblob import TextBlob
from . import app, db
from .models import Tweet

# Configuration de Flask-Restx
api = Api(
    app,
    version='1.0',
    title='Sentiment Analysis API',
    description='API pour analyser le sentiment des tweets',
    doc='/api/docs' 
)

tweet_model = api.model('Tweet', {
    'text': fields.String(required=True, description='Le texte du tweet'),
    'positive': fields.Integer(description='1 si positif, 0 sinon'),
    'negative': fields.Integer(description='1 si négatif, 0 sinon')
})


@api.route('/ping')
class Ping(Resource):
    def get(self):
        """
        Vérifier si l'API est en ligne.
        """
        return jsonify({"status": "ok"})


@api.route('/analyze')
class AnalyzeSentiment(Resource):
    @api.expect(api.model('AnalyzeInput', {
        'tweets': fields.List(fields.String, required=True, description='Liste de tweets à analyser')
    }))
    @api.marshal_with(api.model('AnalyzeOutput', {
        'sentiment_scores': fields.Raw(description='Scores de sentiment pour chaque tweet')
    }))
    def post(self):
        """
        Analyser le sentiment des tweets fournis.
        """
        data = request.json
        tweets = data.get('tweets', [])

        if not tweets:
            return {"error": "No tweets provided"}, 400

        sentiment_scores = {}

        for tweet in tweets:
            analysis = TextBlob(tweet)
            sentiment_scores[tweet] = analysis.sentiment.polarity

            positive = 1 if analysis.sentiment.polarity > 0 else 0
            negative = 1 if analysis.sentiment.polarity < 0 else 0

            new_tweet = Tweet(text=tweet, positive=positive, negative=negative)
            db.session.add(new_tweet)

        db.session.commit()

        return {"sentiment_scores": sentiment_scores}

if __name__ == '__main__':
    app.run(debug=True)
