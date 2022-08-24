'''
nba_bot
~~~~~~~~~~
This file searches for recent mentions of this bot and responds with the stats the Twitter user requested.

@Author: Kevin Tatooles
@Credit: https://www.youtube.com/watch?v=W0wWwglE1Vc for logic on replying to recent Twitter mentions.
'''
import json
import pandas as pd
import tweepy
import gspread
import exceptions

df = None

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
    
    Then fetches all NBA data and parses for the data requested by the user via pandas
    '''
    tokens = request_string.split()

    # Don't respond to tweets that don't start with the @
    if tokens[0] != '@sportstatsgenie':
        raise exceptions.InvalidAtException

    if tokens[1] != 'nba':
        raise exceptions.InvalidLeagueException

    if len(tokens) < 6:
        raise exceptions.NotEnoughArgumentsException

    career = False
    if tokens[4] == 'career':
        career = True

    seasons = [
        '1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02',
        '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08',
        '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14',
        '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20',
        '2020-21', '2021-22'
    ]
    if tokens[4] not in seasons and not career:
        raise exceptions.InvalidSeasonException


    column_names = [
        'player_id', 'player_name', 'nickname', 'team_id', 'team_abbreviation',
        'age', 'gp',  'w', 'l', 'w_pct', 'min', 'fgm', 'fga', 'fg_pct', 'fg3m',
        'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast',
        'tov', 'stl', 'blk', 'blka', 'pf', 'pfd', 'pts',  'plus_minus',
        'nba_fantasy_pts',  'dd2', 'td3', 'wnba_fantasy_pts', 'gp_rank', 'w_rank',
        'l_rank',  'w_pct_rank', 'min_rank', 'fgm_rank', 'fga_rank', 'fg_pct_rank',
        'fg3m_rank', 'fg3a_rank', 'fg3_pct_rank', 'ftm_rank', 'fta_rank', 'ft_pct_rank', 
        'oreb_rank', 'dreb_rank', 'reb_rank', 'ast_rank', 'tov_rank', 'stl_rank',
        'blk_rank', 'blka_rank', 'pf_rank', 'pfd_rank', 'pts_rank', 'plus_minus_rank', 
        'nba_fantasy_pts_rank', 'dd2_rank', 'td3_rank', 'wnba_fantasy_pts_rank',
        'cfid', 'cfparams'
    ]
    # Now the rest of the arguments are stats
    stat_labels = tokens[5:]
    for stat in stat_labels:
        if stat not in column_names:
            raise exceptions.InvalidStatException

    # Slow operations, only want to process once for each execution, and after faster error checks
    global df
    if df is None:
        nba_stats = gc.open("nba-stats").sheet1
        df = pd.DataFrame(nba_stats.get_all_records())

    name = f"{tokens[2]} {tokens[3]}"
    player = df[(df['player_name'] == name)]
    if player.empty:
        raise exceptions.PlayerNotFoundException
        
    if not career:
        season = player[player['season_id'] == tokens[4]]
        if season.empty:
            raise exceptions.SeasonOutOfRangeException

    # Find and fill stat data
    stat_values = []
    for stat_label in stat_labels:
        if career:
            stat = player[[stat_label]].mean().values[0]
            stat = round(stat, 1)
            stat_values.append(f'{stat} {stat_label}')
        else:
            stat_values.append(f'{season.iloc[0][stat_label]} {stat_label}')

    # Want to convert list into a string with oxford comma
    # Ref: https://stackoverflow.com/a/53981846/
    if len(stat_values) < 3:
        stat_str = ' and '.join(stat_values)
    else:
        stat_str = ', '.join(stat_values[:-1]) + ', and ' + stat_values[-1]

    if career:
        string_end = 'for his career'
    else:
        string_end = f'in the {tokens[4]} season'

    return f"{name.title()} averaged {stat_str} {string_end}"


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
        return "ERROR - I could not process your request. Invalid sport, currently supported sport: NBA"
    except exceptions.NotEnoughArgumentsException:
        return "ERROR - I could not process your request. Not enough arguments, I need 6 at least arguments to make a valid query (@sportstatsgenie, league, first_name, last_name, season, stat)"
    except exceptions.PlayerNotFoundException:
        return "ERROR - I could not process your request. The player you requested could not be found"
    except exceptions.InvalidSeasonException:
        return 'ERROR - I could not process your request. The season you provided is invalid. I can provide NBA stats from 1996-97 to 2021-22'
    except exceptions.InvalidStatException:
        return 'ERROR - I could not process you request. You requested a stat that I do not support. See pinned tweet thread for supported stats'
    except exceptions.SeasonOutOfRangeException:
        return 'ERROR - I could not process your request. The player you requested did not play in that season'
    except exceptions.InvalidQueryException:
        return "ERROR - I could not process your request. Couldn\'t complete a valid query with the information you provided"
    except:
        return "ERROR - I could not process your request. Unknown exception occurred"

def process_tweets():
    '''
    Finds the last Tweet this bot replied to, then fetches all mentions to the bot since that tweet, then stores the new last read tweet
    Then process each tweet and respond accordingly
    '''
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