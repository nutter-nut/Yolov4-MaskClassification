import mysql.connector
from tabulate import tabulate

#pandas mysql
import pandas as pd
import mysql.connector

# Setup MySQL connection
db = mysql.connector.connect(
    host="us-cdbr-east-05.cleardb.net",              # your host, usually localhost
    user="bee2562bca911c",            # your username
    password="41039f7c",        # your password
    database="heroku_c24e1a9450f3bbd"     # name of the data base
)   

# You must create a Cursor object. It will let you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
query = "SELECT * FROM `heroku_c24e1a9450f3bbd`.`datamask`"

df = pd.read_sql(query, con=db)
print(df)

