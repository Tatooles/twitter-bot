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