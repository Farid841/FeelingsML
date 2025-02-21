from . import db
from datetime import datetime
import os
import pickle

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(length=255), nullable=False, index=True)
    positive = db.Column(db.Boolean, nullable=False)
    negative = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

def save_model(model, vectorizer, label_type):
    """Save model and vectorizer together"""
    timestamp = datetime.now().strftime("%Y%m%d")
    model_path = f"models/logistic_regression_{label_type}_{timestamp}.pkl"
    
    model_data = {
        'model': model,
        'vectorizer': vectorizer
    }
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)