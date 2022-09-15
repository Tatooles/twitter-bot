import json
import time
import pandas as pd
import mysql.connector
import gspread

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

# gc = gspread.service_account('gspread_credentials.json')
# nba_stats = gc.open("nba-stats").sheet1
# df = pd.DataFrame(nba_stats.get_all_records())

# print(df.head)

cursor = mydb.cursor()
t0 = time.time()
#cursor.execute("SELECT * FROM nbastats")
cursor.execute("insert into nbastats values(1, stephen curry, steph, 1, gsw, 33, 82, 82, 0, .999, 33.42, 33.42, 33.42, .523, 33.42, 33.42, .523, 33.42, 33.42, .523, 12.52, 12.52, 12.52, 12.52, 12.52, 12.52, 12.52, 12.52, 12.52, 12.52, 12.52, 12.52, 12.52, 1, 1, 30.52, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2345, 2021-22)")

myresult = cursor.fetchall()
t1 = time.time()
print(myresult)
print(t1-t0)

#cursor.execute("CREATE TABLE nbastats(player_id INT, player_name VARCHAR(255), nickname VARCHAR(255), team_id INT, team_abbreviation VARCHAR(3), age INT, gp INT, w INT, l INT, w_pct DECIMAL(3,3), min DECIMAL(5,2), fgm DECIMAL(5,2), fga DECIMAL(5,2), fg_pct DECIMAL(3,3), fg3m DECIMAL(5,2), fg3a DECIMAL(5,2), fg3_pct DECIMAL(3,3), ftm DECIMAL(5,2), fta DECIMAL(5,2), ft_pct DECIMAL(3,3), oreb DECIMAL(5,2), dreb DECIMAL(5,2), reb DECIMAL(5,2), ast DECIMAL(5,2), tov DECIMAL(5,2), stl DECIMAL(5,2), blk DECIMAL(5,2), blka DECIMAL(5,2), pf DECIMAL(5,2), pfd DECIMAL(5,2), pts DECIMAL(5,2), plus_minus DECIMAL(5,2), nba_fantasy_pts DECIMAL(5,2), dd2 INT, td3 INT, wnba_fantasy_pts DECIMAL(5,2), gp_rank INT, w_rank INT, l_rank INT, w_pct_rank INT, min_rank INT, fgm_rank INT, fga_rank INT, fg_pct_rank INT, fg3m_rank INT, fg3a_rank INT, fg3_pct_rank INT, ftm_rank INT, fta_rank INT, ft_pct_rank INT, oreb_rank INT, dreb_rank INT, reb_rank INT, ast_rank INT, tov_rank INT, stl_rank INT, blk_rank INT, blka_rank INT, pf_rank INT, pfd_rank INT, pts_rank INT, plus_minus_rank INT, nba_fantasy_pts_rank INT, dd2_rank INT, td3_rank INT, wnba_fantasy_pts_rank INT, cfid INT, cfparams VARCHAR(255), season_id VARCHAR(255));")

'''
player_id INT
player_name VARCHAR(255)
nickname VARCHAR(255)
team_id INT
team_abbreviation VARCHAR(3)
age INT
gp INT
w INT
l INT
w_pct DECIMAL(3,3)
min DECIMAL(5,2)
fgm DECIMAL(5,2)
fga DECIMAL(5,2)
fg_pct DECIMAL(3,3)
fg3m DECIMAL(5,2)
fg3a DECIMAL(5,2)
fg3_pct DECIMAL(3,3)
ftm DECIMAL(5,2)
fta DECIMAL(5,2)
ft_pct DECIMAL(3,3)
oreb DECIMAL(5,2)
dreb DECIMAL(5,2)
reb DECIMAL(5,2)
ast DECIMAL(5,2)
tov DECIMAL(5,2)
stl DECIMAL(5,2)
blk DECIMAL(5,2)
blka DECIMAL(5,2)
pf DECIMAL(5,2)
pfd DECIMAL(5,2)
pts DECIMAL(5,2)
plus_minus DECIMAL(5,2)
nba_fantasy_pts DECIMAL(5,2)
dd2 INT
td3 INT
wnba_fantasy_pts DECIMAL(5,2)
gp_rank INT
w_rank INT
l_rank INT
w_pct_rank INT
min_rank INT
fgm_rank INT
fga_rank INT
fg_pct_rank INT
fg3m_rank INT
fg3a_rank INT
fg3_pct_rank INT
ftm_rank INT
fta_rank INT
ft_pct_rank INT
oreb_rank INT
dreb_rank INT
reb_rank INT
ast_rank INT
tov_rank INT
stl_rank INT
blk_rank INT
blka_rank INT
pf_rank INT
pfd_rank INT
pts_rank INT
plus_minus_rank INT
nba_fantasy_pts_rank INT
dd2_rank INT
td3_rank INT
wnba_fantasy_pts_rank INT
cfid INT
cfparams VARCHAR(255)
season_id VARCHAR(255)
'''

'''
To add all the data to the database it might be smart to just pull it into a dataframe

nba_stats = gc.open("nba-stats").sheet1
df = pd.DataFrame(nba_stats.get_all_records())

and put that dataframe into the database as shown here:
https://www.projectpro.io/recipes/connect-mysql-python-and-import-csv-file-into-mysql-and-create-table

Would save a big hassle of working with credentials of the CSV
'''