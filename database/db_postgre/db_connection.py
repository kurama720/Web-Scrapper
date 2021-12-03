"""Creates database, connection to it and the table"""

import psycopg2
import psycopg2.extras
from psycopg2 import extensions

from scrapper.logger import create_db_logger
from database.db_postgre.constant_data import USERNAME, PASSWORD, EXISTING_DATABASE

LOGGER = create_db_logger()


def create_database():
    """Create database"""
    # Connect to server
    # Type your username, password and existing database
    connection = psycopg2.connect(user=USERNAME,
                                  password=PASSWORD,
                                  host="127.0.0.1",
                                  port="5432",
                                  database=EXISTING_DATABASE)
    connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    with connection.cursor() as cursor:
        # Create database
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'redditdb'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE redditdb')
        # Close connections
        cursor.close()
        connection.close()


def create_connection():
    """Connect to database and return the connection"""
    db_name = 'redditdb'
    # Type your username and password to connect to database reddit_scrapper
    con = psycopg2.connect(
        database=db_name,
        user=USERNAME,
        password=PASSWORD,
        host="127.0.0.1",
        port="5432"
    )
    con.autocommit = True
    return con


def create_table():
    """Create table"""
    with create_connection().cursor() as cursor:
        create_table_author = '''CREATE TABLE IF NOT EXISTS author (
                                 author_id serial NOT NULL PRIMARY KEY,
                                 name VARCHAR NOT NULL UNIQUE,
                                 user_karma VARCHAR,
                                 cake_day VARCHAR,
                                 post_karma VARCHAR,
                                 comment_karma VARCHAR
                              );'''
        create_table_post = '''CREATE TABLE IF NOT EXISTS post (
                              _id VARCHAR NOT NULL UNIQUE PRIMARY KEY,
                              post_url VARCHAR,
                              comments_number VARCHAR,
                              votes_number VARCHAR,
                              post_category VARCHAR,
                              post_date VARCHAR,
                              author_name VARCHAR,
                              CONSTRAINT fk_author_name
                                  FOREIGN KEY (author_name)
                                      REFERENCES author (name) ON DELETE CASCADE ON UPDATE CASCADE
                              );'''

        cursor.execute(create_table_author)
        cursor.execute(create_table_post)


def create_vault():
    create_database()
    create_table()
    LOGGER.info('Database and table created successfully')
