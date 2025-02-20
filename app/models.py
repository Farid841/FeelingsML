from . import db
import datetime

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False, index=True)
    positive = db.Column(db.Boolean, nullable=False, index=True)
    negative = db.Column(db.Boolean, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)