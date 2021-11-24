"""Creates database, connection to it and the table"""

import psycopg2
import psycopg2.extras
from psycopg2 import extensions


def create_database():
    """Create database"""
    # Connect to server
    connection = psycopg2.connect(user="root",
                                  password="12345",
                                  host="127.0.0.1",
                                  port="5432")
    connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    # Create database
    sql_create_database = 'CREATE DATABASE reddit_scrapper'
    cursor.execute(sql_create_database)
    # Close connections
    cursor.close()
    connection.close()


def create_connection():
    """Connect to database and return the connection"""
    db_name = 'reddit_scrapper'
    con = psycopg2.connect(
        database=db_name,
        user="root",
        password="12345",
        host="127.0.0.1",
        port="5432"
    )
    con.autocommit = True
    return con


def create_table():
    """Create table"""
    cursor = create_connection().cursor()
    cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    cursor.execute('SELECT uuid_generate_v4();')
    create_table_author = '''CREATE TABLE IF NOT EXISTS author (
                             author_id serial NOT NULL PRIMARY KEY,
                             name VARCHAR NOT NULL UNIQUE,
                             user_karma VARCHAR NOT NULL,
                             cake_day VARCHAR NOT NULL,
                             post_karma VARCHAR NOT NULL,
                             comment_karma VARCHAR NOT NULL
                          );'''
    create_table_post = '''CREATE TABLE IF NOT EXISTS post (
                          post_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
                          post_url VARCHAR NOT NULL,
                          comments_number VARCHAR NOT NULL,
                          votes_number VARCHAR NOT NULL,
                          post_category VARCHAR NOT NULL,
                          post_date VARCHAR NOT NULL,
                          author_name VARCHAR NOT NULL,
                          CONSTRAINT fk_author_name
                              FOREIGN KEY (author_name)
                                  REFERENCES author (name) ON DELETE CASCADE ON UPDATE CASCADE
                          );'''

    cursor.execute(create_table_author)
    cursor.execute(create_table_post)


def main():
    create_database()
    create_connection()
    create_table()


main()
