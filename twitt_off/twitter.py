'''
Retrieve Tweets, word embeddings and populates a database
'''

import tweepy 
import spacy
from .models import DB, Tweet, User
from os import getenv


# API Keys
TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')

# Twitter authorization
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

# set up the vecors with spacy
nlp = spacy.load('my_model')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector # a numpy array





# take a user and tweets and add both to our database
def add_or_update_user(username):
    '''
    Allows for adding/updating of user to database
    '''
    
    try:
        # get the username
        twitter_user = TWITTER.get_user(username)



        # update the user tweets- get the most recent ones
        # get user id OR if no user id, then add the user to the database
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        # add the user
        DB.session.add(db_user)

        # actually getting tweets here
        tweets = twitter_user.timeline(count=200,
                                        exclude_replies=True,
                                        include_rts=False,
                                        tweet_mode='extended',
                                        )
        # error checking for any new tweets
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # adding the list of tweets to database - assuming all tweets are new
        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, # creates location in database
                            text=tweet.full_text,
                            vect= vectorized_tweet,
                            )  
            # append the tweet to the user id in database
            db_user.tweets.append(db_tweet)
        
    # error for when user does not exist
    except Exception as e: # cast Exception as e for less typing
        print('Error Processing: {}: {}'.format(username, e))
        raise e # lets the rest of the package know about the issue

        
    else: # only executes when the 'try' above works
         # commiting to database
        DB.session.add(db_tweet)


