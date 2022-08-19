# TODO: Add file comment

import tweepy
import gspread
import pandas as pd
import sys

gc = gspread.service_account('credentials.json')

# Open a sheet from a spreadsheet in one go
last_tweet = gc.open("last-tweet-id").sheet1
nba_stats = gc.open("nba-stats").sheet1

consumerKey = 'IODvXnxsaiG8cU7MtY4XZhyLN'
consumerSecret = 'R9uqkxEXxQdmYFxFwdOSIqibi17WLqDH45QDAC337uC6lYcRWQ'

accessToken = '1478092305361952769-SbteiPfJvqvCxQqzdBy76bycKf8eMd'
accessToken_secret = 'lFwfVInbbgJOQ1gmgMmr7U7jHn7ZLygTTcPGrRXJhPg5G'

client = tweepy.Client(consumer_key=consumerKey, consumer_secret=consumerSecret, access_token=accessToken, access_token_secret=accessToken_secret)

def storeId(last_seen_id):
    last_tweet.update('A2', str(last_seen_id))

def retrieveId():
    return int(last_tweet.acell('A2').value)

# This function takes in a request string from the user, and returns what the bot will respond with
def return_stats(request_string):
    # String format @sports_guesses SPORT PLAYER_FIRSTNAME PLAYER_LASTNAME STAT YEAR
    # Example: @sports_guesses NBA Lebron James ppg 2021-22
    tokens = request_string.split()
    if(tokens[1] != 'NBA'):
        return 'ERROR - I could not process your request. Reason: Invalid sport. Please request a valid sport. Currently supported sports: NBA'
    df = pd.DataFrame(nba_stats.get_all_records())
    name = f'{tokens[2]} {tokens[3]}'
    season = df[(df['PLAYER_NAME'] == name) & (df['season_id'] == tokens[4])]
    stat = season.iloc[0][tokens[5]]
    return f'{name} averaged {stat} {tokens[5]} in the {tokens[4]} season'

lastId = retrieveId()
response = client.get_users_mentions(id=1478092305361952769, since_id=lastId, expansions=['author_id'], user_auth=True)
tweets = response.data
if tweets:
    for tweet in reversed(tweets):
        lastId = tweet.id
        storeId(lastId)
        tweet_text = return_stats(tweet.text.lower())
        client.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet.id)

if __name__ == '__main__':
    #df = pd.DataFrame(nba_stats.get_all_records())
    #print(df.query("PLAYER_NAME == `Zach LaVine`"))
    # print('break')
    # # Get all years for a specific player
    # season = df[(df['PLAYER_NAME'] == 'Zach LaVine') & (df['season_id'] == '2020-21')]
    # print(season)
    # print(type(season))
    # print(season.iloc[0]['PTS'])
    print(return_stats(sys.argv[1]))