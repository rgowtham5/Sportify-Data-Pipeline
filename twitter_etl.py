import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 

def run_twitter_etl():

    access_key = "1542552052034945025-qWRIzMb2sXoSMJnybV5e42f0nFG8dx" 
    access_secret = "N7GT7VMmKET1A0QMowHRsfR16r89HbIlFXxU3EaDjSGY0" 
    consumer_key = "QdH3RGn1nst6ytYpKk74ReZbw"
    consumer_secret = "0fXNdsfxIMUgOQ39arS1PHz2d1YVF3TlccGqcHXXtyf0637RZO"

    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@BBCWorld', 
                               count=200,
                               include_rts=False,
                               tweet_mode='extended')

    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                         'text': text,
                         'favorite_count': tweet.favorite_count,
                         'retweet_count': tweet.retweet_count,
                         'created_at': tweet.created_at}
        
        list.append(refined_tweet)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(list)

    # Save the DataFrame to a CSV file in S3
    fs = s3fs.S3FileSystem(anon=False)
    with fs.open('/Users/gowthamramakrishnan/Desktop/refined_tweets.csv', 'w') as f:
        df.to_csv(f, index=False)
