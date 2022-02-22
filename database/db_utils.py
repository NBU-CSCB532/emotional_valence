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
     CREATE TABLE IF NOT EXISTS dictionary (
         id integer PRIMARY KEY,
         WordForm text NOT NULL,
         TranscriptAsFound text NOT NULL)"""
    cur.execute(customers_sql)
    cur.close()

    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS searches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        type VARCHAR NOT NULL,
        query VARCHAR NOT NULL,
        status VARCHAR,
        from_date DATE,
        until_date DATE,
        filename VARCHAR,
        biphone_score DOUBLE
    )""")
    cur.close()

    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR NOT NULL,
        url VARCHAR NOT NULL,
        publish_date DATETIME,
        filename VARCHAR NOT NULL,
        search_id INTEGER NOT NULL,
        vader_score DOUBLE,
        biphone_score DOUBLE,
        FOREIGN KEY(search_id) REFERENCES searches (id)
    )""")
    cur.close()

    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tweet_id VARCHAR,
        text TEXT,
        created_at DATETIME,
        search_id INTEGER NOT NULL,
        vader_score DOUBLE,
        FOREIGN KEY(search_id) REFERENCES searches (id)
    )""")
    cur.close()


