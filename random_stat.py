import json
import tweepy
import mysql.connector

def find_stat():
    with open('railway_credentials.json') as credentials:
        creds = json.load(credentials)

        global mydb
        mydb = mysql.connector.connect(
            host=creds['host'],
            user=creds['user'],
            password=creds['password'],
            database=creds['database'],
            port=creds['port']
        )

    cursor = mydb.cursor(buffered=True)

    cursor.execute("SELECT player_name, pts, reb, ast, fg_pct, fg3_pct, ft_pct, season_id FROM nbastats ORDER BY RAND() LIMIT 1")
    
    data = cursor.fetchall()[0]

    return f'Random stat of the day: {data[0].title()} averaged {data[1]} PPG, {data[2]} RPG, and {data[3]} APG, on {data[4]}, {data[5]}, {data[6]} shooting splits in the {data[7]} season.'

def send_tweet(tweet_text):
    with open('tweepy_credentials.json') as tweepy_credentials:
        creds = json.load(tweepy_credentials)
        client = tweepy.Client(consumer_key=creds['consumerKey'], consumer_secret=creds['consumerSecret'], access_token=creds['accessToken'], access_token_secret=creds['accessToken_secret'])
        client.create_tweet(text=tweet_text)

if __name__ == '__main__':
        send_tweet(find_stat())