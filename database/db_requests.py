"""Module implements processing requests to database."""
from psycopg2 import errors as db_error

from database.db_connection import create_connection
from scrapper.logger import logger_for_handlers

LOGGER = logger_for_handlers()

CONNECTION = create_connection()
CURSOR = CONNECTION.cursor()

AUTHOR_FIELDS = ["author", "user_karma", "cake_day", "post_karma", "comment_karma"]

POST_FIELDS = ['post_id', 'post_url', 'comments_number', 'votes_number', 'post_category', 'post_date']

TOTAL_FIELDS = ['post_id', 'post_url', 'comments_number', 'votes_number', 'post_category', 'post_date', 'author',
                'user_karma', 'cake_day', 'post_karma', 'comment_karma']


def insert_record(data: dict):
    """Insert records in database"""
    try:
        save_author_data = '''INSERT INTO author (name, user_karma, cake_day, post_karma, comment_karma) VALUES
                              (%s, %s, %s, %s, %s)
                           '''
        save_post_data = '''INSERT INTO post (post_id, post_url, comments_number, votes_number, post_category, post_date,
                         author_name) VALUES (%s, %s, %s, %s, %s, %s, %s) 
                         '''
        author_exists = '''SELECT * from author WHERE name = %s'''
        post_data = [v for k, v in data.items() if k in POST_FIELDS]
        post_data.append(data['author'])
        CURSOR.execute(author_exists, (data['author'],))
        if not CURSOR.fetchall():
            CURSOR.execute(save_author_data, ([v for k, v in data.items() if k in AUTHOR_FIELDS]))
        CURSOR.execute(save_post_data, ([i for i in post_data]))
    except db_error:
        LOGGER.error(f"{db_error}")


def find_record(element_id: str = ''):
    """Find records in database, If all_records True then find all of records. Provide taken data with fields and
    return dict"""
    try:
        if not element_id:
            find_all = '''SELECT post_id, post_url, comments_number, votes_number, post_category, post_date, name,
                       user_karma, cake_day, post_karma, comment_karma FROM post INNER JOIN author 
                       ON post.author_name = author.name
                       '''
            CURSOR.execute(find_all)
            data = CURSOR.fetchall()
            output = []
            for data in data:
                named_records = {}
                for i in range(len(TOTAL_FIELDS)):
                    named_records[TOTAL_FIELDS[i]] = data[i]
                output.append(named_records)
            return output
        else:
            find_by_id = '''SELECT post_id, post_url, comments_number, votes_number, post_category, post_date, name,
                       user_karma, cake_day, post_karma, comment_karma FROM post INNER JOIN author 
                       ON post.author_name = author.name WHERE post_id = %s'''
            CURSOR.execute(find_by_id, (element_id,))
            data = CURSOR.fetchall()
            for data in data:
                named_records = {}
                for i in range(len(TOTAL_FIELDS)):
                    named_records[TOTAL_FIELDS[i]] = data[i]
                return named_records
    except db_error:
        LOGGER.error(f"{db_error}")


def update_record(element_id: str, data: dict):
    """Update record with given id and given data. SQL is picky, so every key is to be processed in separate block"""
    try:
        for k, v in data.items():
            k = k.lower()
            if 'post_url' in k:
                update_by_id = '''UPDATE post SET post_url = %s WHERE post_id = %s'''
                CURSOR.execute(update_by_id, (v, element_id,))
            elif 'author' in k:
                update_by_id = '''SELECT * FROM author INNER JOIN post ON author.name = post.author_name
                               WHERE post.post_id = %s;
                               UPDATE author SET name = %s;'''
                CURSOR.execute(update_by_id, (element_id, v))
            elif 'user_karma' in k:
                update_by_id = '''SELECT * FROM author INNER JOIN post ON author.name = post.author_name
                               WHERE post.post_id = %s;
                               UPDATE author SET user_karma = %s;'''
                CURSOR.execute(update_by_id, (element_id, v))
            elif 'cake_day' in k:
                update_by_id = '''SELECT * FROM author INNER JOIN post ON author.name = post.author_name
                               WHERE post.post_id = %s;
                               UPDATE author SET cake_day = %s;'''
                CURSOR.execute(update_by_id, (element_id, v))
            elif 'comments_number' in k:
                update_by_id = '''UPDATE post SET comments_number = %s WHERE post_id = %s'''
                CURSOR.execute(update_by_id, (v, element_id,))
            elif 'votes_number' in k:
                update_by_id = '''UPDATE post SET votes_number = %s WHERE post_id = %s'''
                CURSOR.execute(update_by_id, (v, element_id,))
            elif 'post_category' in k:
                update_by_id = '''UPDATE post SET post_category = %s WHERE post_id = %s'''
                CURSOR.execute(update_by_id, (v, element_id,))
            elif 'post_karma' in k:
                update_by_id = '''SELECT * FROM author INNER JOIN post ON author.name = post.author_name
                               WHERE post.post_id = %s;
                               UPDATE author SET post_karma = %s;'''
                CURSOR.execute(update_by_id, (element_id, v))
            elif 'comment_karma' in k:
                update_by_id = '''SELECT * FROM author INNER JOIN post ON author.name = post.author_name
                               WHERE post.post_id = %s;
                               UPDATE author SET comment_karma = %s;'''
                CURSOR.execute(update_by_id, (element_id, v))
            elif 'post_date' in k:
                update_by_id = '''UPDATE post SET post_date = %s WHERE post_id = %s'''
                CURSOR.execute(update_by_id, (v, element_id,))
    except db_error:
        LOGGER.error(f"{db_error}")


def delete_record(element_id: str):
    """Delete record with given id"""
    try:
        # Find author name
        CURSOR.execute('''SELECT author_name FROM post WHERE post_id = %s''', (element_id,))
        author_name = CURSOR.fetchone()
        # Delete post with given id
        delete_by_id = '''DELETE FROM post WHERE post_id = %s'''
        CURSOR.execute(delete_by_id, (element_id,))
        # Find all posts by the author found previously
        CURSOR.execute('''SELECT post_id FROM post WHERE author_name = %s''', author_name)
        author_has_posts = CURSOR.fetchall()
        # Check whether he has posts and delete if False
        if not author_has_posts:
            CURSOR.execute('''DELETE FROM author WHERE name = %s''', author_name)
    except db_error:
        LOGGER.error(f"{db_error}")