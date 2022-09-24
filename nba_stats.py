'''
nba_stats
~~~~~~~~~~
This file scrapes the NBA stats api on stat.nba.com and stores the data in a Google Sheet via a Pandas Dataframe.

@Author: Kevin Tatooles
@Credit: https://www.youtube.com/watch?v=IELK56jIsEo&t=752s for scraping the NBA website.
'''
from time import time
import requests
import pandas as pd
import gspread
import numpy as np
import json
import mysql.connector
import time

def setup():
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

        global cursor
        cursor = mydb.cursor(buffered=True)

def fetch_data(seasons):
    '''
    Calls out to the NBA api once for each available season, then combines all the data into a single dataframe.

    :param list seasons: Which NBA season to retrieve data for
    :returns DataFrame df: A dataframe containg all stat data from stats.nba.com 
    '''
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # All the stats we will store
    column_names = [
        'PLAYER_ID',
        'PLAYER_NAME',
        'NICKNAME',
        'TEAM_ID',
        'TEAM_ABBREVIATION',
        'AGE',
        'GP', 
        'W',
        'L',
        'W_PCT',
        'MIN',
        'FGM',
        'FGA',
        'FG_PCT',
        'FG3M',
        'FG3A',
        'FG3_PCT',
        'FTM',
        'FTA',
        'FT_PCT',
        'OREB',
        'DREB',
        'REB',
        'AST',
        'TOV',
        'STL',
        'BLK',
        'BLKA',
        'PF',
        'PFD',
        'PTS', 
        'PLUS_MINUS',
        'NBA_FANTASY_PTS', 
        'DD2',
        'TD3', 
        'WNBA_FANTASY_PTS', 
        'GP_RANK',
        'W_RANK',
        'L_RANK', 
        'W_PCT_RANK',
        'MIN_RANK',
        'FGM_RANK',
        'FGA_RANK',
        'FG_PCT_RANK',
        'FG3M_RANK', 
        'FG3A_RANK',
        'FG3_PCT_RANK',
        'FTM_RANK',
        'FTA_RANK',
        'FT_PCT_RANK', 
        'OREB_RANK',
        'DREB_RANK',
        'REB_RANK', 
        'AST_RANK',
        'TOV_RANK',
        'STL_RANK',
        'BLK_RANK',
        'BLKA_RANK',
        'PF_RANK',
        'PFD_RANK', 
        'PTS_RANK',
        'PLUS_MINUS_RANK', 
        'NBA_FANTASY_PTS_RANK',
        'DD2_RANK',
        'TD3_RANK',
        'WNBA_FANTASY_PTS_RANK',
        'CFID', 
        'CFPARAMS'
    ]

    season_data = []

    count = 0
    t0 = time.time()

    for season in seasons:
        request_url = f"https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={season}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
        response = requests.get(url=request_url, headers=headers).json()
        player_info = response['resultSets'][0]['rowSet']
        # numpy = np.asarray(player_info)
        # numpy = np.delete(numpy, [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65], axis=1)
        # print(numpy)
        # Remove columns from 36 to 65, that's like half of it lmao
        for row in player_info:
            row.append(season)
            sql = "insert into nbastats values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, row)
            mydb.commit()
            print(f"Inserted record {count} of 12475")
            count += 1
        
        # break
        # df = pd.DataFrame(player_info, columns=column_names)
        # df['season_id'] = season
        # print(season)
        # season_data.append(df)

    print(f"Total time: {time.time() - t0}")

    # return pd.concat(season_data, sort=False)


def save_data(data):
    '''
    Takes the dataframe and saves it into google sheets.

    :param data: NBA stat data in the form of a dataframe
    '''
    gc = gspread.service_account('gspread_credentials.json')

    # Open a sheet from a spreadsheet in one go
    nba_stats = gc.open("nba-stats").sheet1

    # Save data to spreadsheet
    nba_stats.update([data.columns.values.tolist()] + data.values.tolist())


if __name__ == '__main__':
    seasons = [
        '1996-97',
        '1997-98',
        '1998-99',
        '1999-00',
        '2000-01',
        '2001-02',
        '2002-03',
        '2003-04',
        '2004-05',
        '2005-06',
        '2006-07',
        '2007-08',
        '2008-09',
        '2009-10',
        '2010-11',
        '2011-12',
        '2012-13',
        '2013-14',
        '2014-15',
        '2015-16',
        '2016-17',
        '2017-18',
        '2018-19',
        '2019-20',
        '2020-21',
        '2021-22'
    ]
    
    setup()
    fetch_data(seasons)
    # Convert all text data to lowercase because tweet will be converted to lowercase
    # data = data.applymap(lambda s: s.lower() if type(s) == str else s)
    # # Want columns also lowercase
    # data.columns = data.columns.str.lower()
    # save_data(data)
    