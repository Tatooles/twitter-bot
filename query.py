import json
import mysql.connector

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

cursor = mydb.cursor()

cursor.execute("SELECT * FROM test_table_2")

myresult = cursor.fetchall()

print(myresult)

'''
To add all the data to the database it might be smart to just pull it into a dataframe

nba_stats = gc.open("nba-stats").sheet1
df = pd.DataFrame(nba_stats.get_all_records())

and put that dataframe into the database as shown here:
https://www.projectpro.io/recipes/connect-mysql-python-and-import-csv-file-into-mysql-and-create-table

Would save a big hassle of working with credentials of the CSV
'''