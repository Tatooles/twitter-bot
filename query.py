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

gc = gspread.service_account('gspread_credentials.json')
nba_stats = gc.open("nba-stats").sheet1
df = pd.DataFrame(nba_stats.get_all_records())

t0 = time.time()
cursor = mydb.cursor()

# for i,row in df.iterrows():
#     sql = "insert into nbastats values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
#     val = tuple(row)
#     cursor.execute(sql, val)
#     mydb.commit()
#     print("record inserted")

'''
This code creates the table
#cursor.execute("CREATE TABLE nbastats(player_id VARCHAR(255), player_name VARCHAR(255), nickname VARCHAR(255), team_id VARCHAR(255), team_abbreviation VARCHAR(3), age VARCHAR(255), gp VARCHAR(255), w VARCHAR(255), l VARCHAR(255), w_pct VARCHAR(255), min VARCHAR(255), fgm VARCHAR(255), fga VARCHAR(255), fg_pct VARCHAR(255), fg3m VARCHAR(255), fg3a VARCHAR(255), fg3_pct VARCHAR(255), ftm VARCHAR(255), fta VARCHAR(255), ft_pct VARCHAR(255), oreb VARCHAR(255), dreb VARCHAR(255), reb VARCHAR(255), ast VARCHAR(255), tov VARCHAR(255), stl VARCHAR(255), blk VARCHAR(255), blka VARCHAR(255), pf VARCHAR(255), pfd VARCHAR(255), pts VARCHAR(255), plus_minus VARCHAR(255), nba_fantasy_pts VARCHAR(255), dd2 VARCHAR(255), td3 VARCHAR(255), wnba_fantasy_pts VARCHAR(255), gp_rank VARCHAR(255), w_rank VARCHAR(255), l_rank VARCHAR(255), w_pct_rank VARCHAR(255), min_rank VARCHAR(255), fgm_rank VARCHAR(255), fga_rank VARCHAR(255), fg_pct_rank VARCHAR(255), fg3m_rank VARCHAR(255), fg3a_rank VARCHAR(255), fg3_pct_rank VARCHAR(255), ftm_rank VARCHAR(255), fta_rank VARCHAR(255), ft_pct_rank VARCHAR(255), oreb_rank VARCHAR(255), dreb_rank VARCHAR(255), reb_rank VARCHAR(255), ast_rank VARCHAR(255), tov_rank VARCHAR(255), stl_rank VARCHAR(255), blk_rank VARCHAR(255), blka_rank VARCHAR(255), pf_rank VARCHAR(255), pfd_rank VARCHAR(255), pts_rank VARCHAR(255), plus_minus_rank VARCHAR(255), nba_fantasy_pts_rank VARCHAR(255), dd2_rank VARCHAR(255), td3_rank VARCHAR(255), wnba_fantasy_pts_rank VARCHAR(255), cfid VARCHAR(255), cfparams VARCHAR(255), season_id VARCHAR(255));")

This code adds a single row to the table
sql = "insert into nbastats values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
val = ("1", "stephen curry", "steph", "1", "gsw", "33", "82", "82", "0", "0.999", "33.42", "33.42", "33.42", "0.523", "33.42", "33.42", "0.523", "33.42", "33.42", "0.523", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "1", "1", "30.52", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2345", "1999")
cursor.execute(sql, val)
mydb.commit()
'''

# cursor.execute("CREATE TABLE nbastats (player_id INT, player_name VARCHAR(255), nickname VARCHAR(255), team_id VARCHAR(255), team_abbreviation VARCHAR(3), age INT, gp INT, w INT, l INT, w_pct DECIMAL, min DECIMAL, fgm DECIMAL, fga DECIMAL, fg_pct DECIMAL, fg3m DECIMAL, fg3a DECIMAL, fg3_pct DECIMAL, ftm DECIMAL, fta DECIMAL, ft_pct DECIMAL, oreb DECIMAL, dreb DECIMAL, reb DECIMAL, ast DECIMAL, tov DECIMAL, stl DECIMAL, blk DECIMAL, blka DECIMAL, pf DECIMAL, pfd DECIMAL, pts DECIMAL, plus_minus DECIMAL, nba_fantasy_pts DECIMAL, dd2 INT, td3 INT, wnba_fantasy_pts DECIMAL, gp_rank INT, w_rank INT, l_rank INT, w_pct_rank INT, min_rank INT, fgm_rank INT, fga_rank INT, fg_pct_rank INT, fg3m_rank INT, fg3a_rank INT, fg3_pct_rank INT, ftm_rank INT, fta_rank INT, ft_pct_rank INT, oreb_rank INT, dreb_rank INT, reb_rank INT, ast_rank INT, tov_rank INT, stl_rank INT, blk_rank INT, blka_rank INT, pf_rank INT, pfd_rank INT, pts_rank INT, plus_minus_rank INT, nba_fantasy_pts_rank INT, dd2_rank INT, td3_rank INT, wnba_fantasy_pts_rank INT, cfid INT, cfparams VARCHAR(255), season_id VARCHAR(255));")

# cursor.execute("DROP TABLE nbastats")
cursor.execute("SELECT player_name, pts FROM nbastats where player_name = %s", ("stephen curry",))
# cursor.execute("DELETE FROM nbastats")
myresult = cursor.fetchall()
print(myresult)
print(time.time() - t0)

'''
player_id VARCHAR(255)
player_name VARCHAR(255)
nickname VARCHAR(255)
team_id VARCHAR(255)
team_abbreviation VARCHAR(3)
age VARCHAR(255)
gp VARCHAR(255)
w VARCHAR(255)
l VARCHAR(255)
w_pct VARCHAR(255)
min VARCHAR(255)
fgm VARCHAR(255)
fga VARCHAR(255)
fg_pct VARCHAR(255)
fg3m VARCHAR(255)
fg3a VARCHAR(255)
fg3_pct VARCHAR(255)
ftm VARCHAR(255)
fta VARCHAR(255)
ft_pct VARCHAR(255)
oreb VARCHAR(255)
dreb VARCHAR(255)
reb VARCHAR(255)
ast VARCHAR(255)
tov VARCHAR(255)
stl VARCHAR(255)
blk VARCHAR(255)
blka VARCHAR(255)
pf VARCHAR(255)
pfd VARCHAR(255)
pts VARCHAR(255)
plus_minus VARCHAR(255)
nba_fantasy_pts VARCHAR(255)
dd2 VARCHAR(255)
td3 VARCHAR(255)
wnba_fantasy_pts VARCHAR(255)
gp_rank VARCHAR(255)
w_rank VARCHAR(255)
l_rank VARCHAR(255)
w_pct_rank VARCHAR(255)
min_rank VARCHAR(255)
fgm_rank VARCHAR(255)
fga_rank VARCHAR(255)
fg_pct_rank VARCHAR(255)
fg3m_rank VARCHAR(255)
fg3a_rank VARCHAR(255)
fg3_pct_rank VARCHAR(255)
ftm_rank VARCHAR(255)
fta_rank VARCHAR(255)
ft_pct_rank VARCHAR(255)
oreb_rank VARCHAR(255)
dreb_rank VARCHAR(255)
reb_rank VARCHAR(255)
ast_rank VARCHAR(255)
tov_rank VARCHAR(255)
stl_rank VARCHAR(255)
blk_rank VARCHAR(255)
blka_rank VARCHAR(255)
pf_rank VARCHAR(255)
pfd_rank VARCHAR(255)
pts_rank VARCHAR(255)
plus_minus_rank VARCHAR(255)
nba_fantasy_pts_rank VARCHAR(255)
dd2_rank VARCHAR(255)
td3_rank VARCHAR(255)
wnba_fantasy_pts_rank VARCHAR(255)
cfid VARCHAR(255)
cfparams VARCHAR(255)
season_id VARCHAR(255)
'''

'''
player_id INT, player_name VARCHAR(255), nickname VARCHAR(255), team_id VARCHAR(255), team_abbreviation VARCHAR(3), age INT, gp INT, w INT, l INT, w_pct DECIMAL, min DECIMAL, fgm DECIMAL, fga DECIMAL, fg_pct DECIMAL, fg3m DECIMAL, fg3a DECIMAL, fg3_pct DECIMAL, ftm DECIMAL, fta DECIMAL, ft_pct DECIMAL, oreb DECIMAL, dreb DECIMAL, reb DECIMAL, ast DECIMAL, tov DECIMAL, stl DECIMAL, blk DECIMAL, blka DECIMAL, pf DECIMAL, pfd DECIMAL, pts DECIMAL, plus_minus DECIMAL, nba_fantasy_pts DECIMAL, dd2 INT, td3 INT, wnba_fantasy_pts DECIMAL, gp_rank INT, w_rank INT, l_rank INT, w_pct_rank INT, min_rank INT, fgm_rank INT, fga_rank INT, fg_pct_rank INT, fg3m_rank INT, fg3a_rank INT, fg3_pct_rank INT, ftm_rank INT, fta_rank INT, ft_pct_rank INT, oreb_rank INT, dreb_rank INT, reb_rank INT, ast_rank INT, tov_rank INT, stl_rank INT, blk_rank INT, blka_rank INT, pf_rank INT, pfd_rank INT, pts_rank INT, plus_minus_rank INT, nba_fantasy_pts_rank INT, dd2_rank INT, td3_rank INT, wnba_fantasy_pts_rank INT, cfid INT, cfparams VARCHAR(255), season_id VARCHAR(255)
'''

'''
("1", "stephen curry", "steph", "1", "gsw", "33", "82", "82", "0", "0.999", "33.42", "33.42", "33.42", "0.523", "33.42", "33.42", "0.523", "33.42", "33.42", "0.523", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "12.52", "1", "1", "30.52", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2345", "1999")
'''

'''
To add all the data to the database it might be smart to just pull it into a dataframe

nba_stats = gc.open("nba-stats").sheet1
df = pd.DataFrame(nba_stats.get_all_records())

and put that dataframe into the database as shown here:
https://www.projectpro.io/recipes/connect-mysql-python-and-import-csv-file-into-mysql-and-create-table

Would save a big hassle of working with credentials of the CSV
'''