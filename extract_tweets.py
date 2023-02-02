import tweepy
import pandas as pd
from tweepy import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('api_key')
api_key_secret = os.environ.get('api_key_secret')
access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')

auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

def pre_process(tweet):
    processed_tweet = []
    for word in tweet.split():
        if word.startswith('@') and len(word) > 1:
           word = word[1:] 
        if not word.startswith('https://'):
            processed_tweet.append(word)
    return  " ".join(processed_tweet)


def extract_tweets(keyword,date_since,date_until,num_tweets=300):
    tweets = tweepy.Cursor(
                            api.search_tweets,
                            keyword, lang="en",
                            since_id=date_since,
                            until=date_until,
                            tweet_mode='extended').items(num_tweets)
    tweet_cont,tweet_rt,tweet_heart=[],[],[]
    for tweet in tweets:
        try:
            tweet_cont.append(pre_process(tweet.full_text))
            tweet_rt.append(tweet.retweet_count)
            tweet_heart.append(tweet.retweeted_status.favorite_count)
        except AttributeError:
            tweet_heart.append(0)
    data = {
        'Tweet': tweet_cont,
        'Retweet': tweet_rt,
        'Favs':tweet_heart
            }
    return pd.DataFrame(data)
