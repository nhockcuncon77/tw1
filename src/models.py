from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import backref
#import Spacy

db = SQLAlchemy()

# Creates a 'user' table


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id as primary key
    name = db.Column(db.String(50), nullable=False)  # user name

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode(300))
    tweet_vect = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey(
        "user.id"), nullable=False)
    user = db.relationship('User', backref=db.backref("tweet", lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)
