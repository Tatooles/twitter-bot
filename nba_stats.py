'''
nba_stats
~~~~~~~~~~
This file scrapes the NBA stats api on stat.nba.com and stores the data in a Google Sheet via a Pandas Dataframe.

@Author: Kevin Tatooles
@Credit: https://www.youtube.com/watch?v=IELK56jIsEo&t=752s for scraping the NBA website.
'''
import requests
import json
import mysql.connector

def setup():
    '''
    Initializes connection with the MySQL database.
    '''
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

    for season in seasons:
        request_url = f"https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={season}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
        response = requests.get(url=request_url, headers=headers).json()
        player_info = response['resultSets'][0]['rowSet']
        
        # Go through each player from that season and add to DB
        for row in player_info:
            # Only want the stats that matter
            row = row[:35]
            row.append(season)
            sql = "insert into nbastats values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, tuple(row))
            mydb.commit()


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
    