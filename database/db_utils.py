import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def init_database():
    con = db_connect() # connect to the database
    cur = con.cursor() # instantiate a cursor obj
    customers_sql = """
     CREATE TABLE dictionary (
         id integer PRIMARY KEY,
         WordForm text NOT NULL,
         TranscriptAsFound text NOT NULL)"""
    cur.execute(customers_sql)
    cur.close()
