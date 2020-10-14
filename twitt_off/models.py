'''
SQLAlchmey models and utility functions for TwitOff
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# create a database
DB = SQLAlchemy()

# create a table
class User(DB.Model):
    '''
    Twitter Users Corresponding to Tweets
    '''
    # create columns with SQLAlchemy syntax
    id = DB. Column(DB.BigInteger, primary_key=True) # id column
    name = DB.Column(DB.String, nullable=False)# name column
    newest_tweet_id = DB.Column(DB.BigInteger) # store most recent tweet

    # representation method
    def __repr__(self):
        return '<User: {}>'.format(self.name)


# new table - Tweets
class Tweet(DB.Model):
    '''
    Tweet related to a user
    '''
    id = DB. Column(DB.BigInteger, primary_key=True) # id column
    text = DB.Column(DB.Unicode(300)) # allowing for actual text
    vect = DB.Column(DB.PickleType, nullable=False)

    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False) # relates to key in User class
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet: {}>'.format(self.text)
