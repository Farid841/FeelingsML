from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from textblob import TextBlob

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/sentiment_analysis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy et Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modèle de la table `tweets`
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    positive = db.Column(db.Boolean, nullable=False)
    negative = db.Column(db.Boolean, nullable=False)

# Endpoint GET pour tester si l'API est opérationnelle
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})

# Endpoint POST pour l'analyse des sentiments
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

        # Enregistrer le tweet dans la base de données
        positive = 1 if analysis.sentiment.polarity > 0 else 0
        negative = 1 if analysis.sentiment.polarity < 0 else 0

        new_tweet = Tweet(text=tweet, positive=positive, negative=negative)
        db.session.add(new_tweet)

    db.session.commit()

    return jsonify(sentiment_scores)

if __name__ == '__main__':
    app.run(debug=True)