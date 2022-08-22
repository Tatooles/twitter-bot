import json
import random
import pandas as pd
import tweepy
import gspread

def find_stat():
    gc = gspread.service_account('gspread_credentials.json')
    nba_stats = gc.open("nba-stats").sheet1
    df = pd.DataFrame(nba_stats.get_all_records())

    # Get random row
    row = random.randint(0, len(df.index))
    
    # TODO: Now figure out what stat to print
    # Choose a totally random stat or a random relevant one?
    # Or tweet out the player's whole statline?

def send_tweet(tweet_text):
    with open('tweepy_credentials.json') as tweepy_credentials:
        creds = json.load(tweepy_credentials)
        client = tweepy.Client(consumer_key=creds['consumerKey'], consumer_secret=creds['consumerSecret'], access_token=creds['accessToken'], access_token_secret=creds['accessToken_secret'])
        client.create_tweet(text=tweet_text)

if __name__ == '__main__':
    find_stat()