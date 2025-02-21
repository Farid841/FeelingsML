import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import request, jsonify
from flask_restx import Api, Resource, fields
from textblob import TextBlob
from . import app, db
from .models import Tweet

# Load the trained models and vectorizer
def load_latest_model():
    """Load the most recent model files"""
    try:
        model_files = os.listdir('models')
        pos_files = [f for f in model_files if 'positive' in f]
        neg_files = [f for f in model_files if 'negative' in f]
        
        latest_pos = sorted(pos_files)[-1]
        latest_neg = sorted(neg_files)[-1]
        
        with open(f'models/{latest_pos}', 'rb') as f:
            pos_data = pickle.load(f)
            
        with open(f'models/{latest_neg}', 'rb') as f:
            neg_data = pickle.load(f)
            
        return pos_data['model'], neg_data['model'], pos_data['vectorizer']
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return None, None, None

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
    def post(self):
        try:
            data = request.json
            tweets = data.get('tweets', [])

            if not tweets:
                return {"error": "No tweets provided"}, 400

            # Load models and vectorizer
            model_pos, model_neg, vectorizer = load_latest_model()
            
            if not all([model_pos, model_neg, vectorizer]):
                return {"error": "Models not loaded properly"}, 500

            # Vectorize tweets
            X = vectorizer.transform(tweets)

            sentiment_scores = {}

            # Get predictions
            positive_pred = model_pos.predict_proba(X)
            negative_pred = model_neg.predict_proba(X)

            for i, tweet in enumerate(tweets):
                pos_score = float(positive_pred[i][1])
                neg_score = float(negative_pred[i][1])

                sentiment_scores[tweet] = {
                    'positive_score': pos_score,
                    'negative_score': neg_score
                }

                # Save to database
                new_tweet = Tweet(
                    text=tweet,
                    positive=1 if pos_score > 0.5 else 0,
                    negative=1 if neg_score > 0.5 else 0
                )
                db.session.add(new_tweet)

            db.session.commit()
            return {"sentiment_scores": sentiment_scores}

        except Exception as e:
            db.session.rollback()
            print(f"Error in analyze: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}, 500
        
if __name__ == '__main__':
    app.run(debug=True)
