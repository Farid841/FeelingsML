from . import db

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    positive = db.Column(db.Boolean, nullable=False)
    negative = db.Column(db.Boolean, nullable=False)