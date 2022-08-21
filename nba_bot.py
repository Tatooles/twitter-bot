# TODO: Add file comment

import sys
import json
import pandas as pd
import tweepy
import gspread
import exceptions

def setup():
    '''
    Initialize a couple of global variables that will be used during execution.
    '''
    global gc
    gc = gspread.service_account('gspread_credentials.json')

    # Open a sheet from a spreadsheet in one go
    global last_tweet
    last_tweet = gc.open("last-tweet-id").sheet1

    with open('tweepy_credentials.json') as tweepy_credentials:
        creds = json.load(tweepy_credentials)

        global client
        client = tweepy.Client(consumer_key=creds['consumerKey'], consumer_secret=creds['consumerSecret'], access_token=creds['accessToken'], access_token_secret=creds['accessToken_secret'])

def storeId(last_seen_id):
    last_tweet.update('A2', str(last_seen_id))

def retrieveId():
    return int(last_tweet.acell('A2').value)

def check_tweet(request_string):
    '''
    Checks the request string for errors, and throws the appropriate error to be handled by the return string.
    '''
    tokens = request_string.split()
    # FIXME: Maybe only have the bot process input after the @sportstatsgenie so users can use the bot in threads
    # For now just don't respond to tweets in this case
    if tokens[0] != '@sportstatsgenie':
        raise exceptions.InvalidAtException

    if tokens[1] != 'nba':
        raise exceptions.InvalidLeagueException

    if len(tokens) != 6:
        raise exceptions.InvalidArgumentCountException

    # FIXME: Slow operations, only want to execute once rather than for each tweet
    nba_stats = gc.open("nba-stats").sheet1
    df = pd.DataFrame(nba_stats.get_all_records())
    name = f"{tokens[2]} {tokens[3]}"
    player = df[(df['player_name'] == name)]
    if player.empty:
        raise exceptions.PlayerNotFoundException
        
    try:
        if tokens[4] == 'career':
            stat = player[[tokens[5]]].mean().values[0]
            stat = round(stat, 1)
            return f"{tokens[2].capitalize()} {tokens[3].capitalize()} averaged {stat} {tokens[5]} for his career"
        else:
            season = player[player['season_id'] == tokens[4]]
            stat = season.iloc[0][tokens[5]]
            return f"{tokens[2].capitalize()} {tokens[3].capitalize()} averaged {stat} {tokens[5]} in the {tokens[4]} season"
    except:
        raise exceptions.InvalidQueryException


def process_request(request_string):
    '''
    This function takes in a request string from the user, and returns what the bot will respond with

    String format: @sportstatsgenie SPORT PLAYER_FIRSTNAME PLAYER_LASTNAME STAT YEAR

    Example: @sports_guesses NBA Lebron James ppg 2021-22

    :param request_string: The input from twitter of what the user
    '''
    request_string = request_string.lower()
    try:
        return check_tweet(request_string)
    except exceptions.InvalidAtException:
        return
    except exceptions.InvalidLeagueException:
        return "ERROR - I could not process your request. Please request a valid sport. Currently supported sport: NBA"
    except exceptions.InvalidArgumentCountException:
        return "ERROR - I could not process your request. Incorrect number of arguments, I need 6 arguments to make a valid query (@sportstatsgenie, league, first_name, last_name, season, stat)"
    except exceptions.InvalidQueryException:
        return "ERROR - I could not process your request. Couldn\'t complete a valid query with the information you provided"
    except exceptions.PlayerNotFoundException:
        return "ERROR - I could not process your request. The player you requested could not be found"
    except:
        return "ERROR - I could not process your request. Unknown exception occurred"

def process_tweets():
    lastId = retrieveId()
    response = client.get_users_mentions(id=1478092305361952769, since_id=lastId, expansions=['author_id'], user_auth=True)
    tweets = response.data
    if tweets:
        for tweet in reversed(tweets):
            lastId = tweet.id
            storeId(lastId)
            tweet_text = process_request(tweet.text)
            if tweet_text:
                client.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet.id)

if __name__ == '__main__':
    setup()
    process_tweets()