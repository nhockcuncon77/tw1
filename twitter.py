"""Retrieves tweets, embeddings, and persists inthe database"""
from os import getenv
import tweepy
from .models import DB, Tweet, User
import spacy


def add_or_update_user(username):
    try:

        """Add or update a user and their Tweets, error if not a Twitter user."""
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        db.session.add(db_user)
        # Lets get the tweets - focusing on primary (not retweet/reply)
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended'
        )
        for tweet in tweets:
            embedding = vectorize_tweet(tweet.full_text)
            db_tweets = Tweet(
                id=tweet.id, text=tweet.full_text[:300], embedding=embedding)
            db_user.tweets.append(db_tweets)
            DB.session.add(db_tweets)
    except Exception as e:
        print("Error Processing {}: {}".format(db_user, e))
        raise e
    else:
        db.session.commit()
