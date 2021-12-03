"""Module implements processing requests to database."""

from typing import NoReturn, Any

from psycopg2 import errors

from database.postgre.db_connection import create_connection
from scrapper.logger import create_db_logger

LOGGER = create_db_logger()

CONNECTION = create_connection()

AUTHOR_FIELDS = ["author", "user_karma", "cake_day", "post_karma", "comment_karma"]

POST_FIELDS = ['_id', 'post_url', 'comments_number', 'votes_number', 'post_category', 'post_date']

TOTAL_FIELDS = ['_id', 'post_url', 'comments_number', 'votes_number', 'post_category', 'post_date', 'author',
                'user_karma', 'cake_day', 'post_karma', 'comment_karma']

UniqueViolationError = errors.lookup('23505')


def insert_record(data: dict) -> NoReturn:
    """Insert records in database

    :param dict data: data to be inserted
    """
    with CONNECTION.cursor() as cursor:
        try:
            save_author_data = '''INSERT INTO author (name, user_karma, cake_day, post_karma, comment_karma) VALUES
                                  (%s, %s, %s, %s, %s)
                               '''
            save_post_data = '''INSERT INTO post (_id, post_url, comments_number, votes_number, post_category,
                             post_date, author_name) VALUES (%s, %s, %s, %s, %s, %s, %s) 
                             '''
            author_exists = '''SELECT * from author WHERE name = %s'''
            post_data = [v for k, v in data.items() if k in POST_FIELDS]
            post_data.append(data['author'])
            cursor.execute(author_exists, (data['author'],))
            if not cursor.fetchall():
                cursor.execute(save_author_data, ([v for k, v in data.items() if k in AUTHOR_FIELDS]))
            cursor.execute(save_post_data, ([i for i in post_data]))
        except UniqueViolationError:
            raise UniqueViolationError
        except Exception as ex:
            LOGGER.error(f"{ex}")
            raise ex


def find_record(element_id: str = '') -> Any[list, dict]:
    """Find records in database, If all_records True then find all of records. Provide taken data with fields and
    return dict

    :param str element_id: record with _id to be found
    :return: list with dictionaries of records or a dict with one record
    """
    with CONNECTION.cursor() as cursor:
        try:
            if not element_id:
                find_all = '''SELECT _id, post_url, comments_number, votes_number, post_category, post_date, name,
                           user_karma, cake_day, post_karma, comment_karma FROM post INNER JOIN author 
                           ON post.author_name = author.name
                           '''
                cursor.execute(find_all)
                data = cursor.fetchall()
                output = []
                for data in data:
                    named_records = {}
                    for i in range(len(TOTAL_FIELDS)):
                        named_records[TOTAL_FIELDS[i]] = data[i]
                    output.append(named_records)
                return output
            else:
                find_by_id = '''SELECT _id, post_url, comments_number, votes_number, post_category, post_date, name,
                           user_karma, cake_day, post_karma, comment_karma FROM post INNER JOIN author 
                           ON post.author_name = author.name WHERE _id = %s'''
                cursor.execute(find_by_id, (element_id,))
                data = cursor.fetchall()
                for data in data:
                    named_records = {}
                    for i in range(len(TOTAL_FIELDS)):
                        named_records[TOTAL_FIELDS[i]] = data[i]
                    return named_records
        except Exception as ex:
            LOGGER.error(f"{ex}")
            raise ex


def update_record(element_id: str, data: dict) -> NoReturn:
    """Update record with given id and given data. Search for post with element_id and update with given data.

    :param str element_id: _id in post table
    :param dict data: new data for post
    """
    with CONNECTION.cursor() as cursor:
        try:
            for k, v in data.items():
                if k in POST_FIELDS:
                    update_post = """UPDATE post SET {0} = %s WHERE _id = %s""".format(k)
                    cursor.execute(update_post, (v, element_id))
                if k in AUTHOR_FIELDS:
                    update_author = """SELECT * FROM author INNER JOIN post ON author.name = post.author_name
                                   WHERE post._id = %s;
                                   UPDATE author SET {0} = %s;""".format(k)
                    cursor.execute(update_author, (element_id, v))
        except Exception as ex:
            LOGGER.error(f"{ex}")
            raise ex


def delete_record(element_id: str) -> NoReturn:
    """Delete record with given id.

    :param str element_id: record with _id to be deleted
    """
    with CONNECTION.cursor() as cursor:
        try:
            # Find author name
            cursor.execute('''SELECT author_name FROM post WHERE _id = %s''', (element_id,))
            author_name = cursor.fetchone()
            # Delete post with given id
            delete_by_id = '''DELETE FROM post WHERE _id = %s'''
            cursor.execute(delete_by_id, (element_id,))
            # Find all posts by the author found previously
            cursor.execute('''SELECT _id FROM post WHERE author_name = %s''', author_name)
            author_has_posts = cursor.fetchall()
            # Check whether he has posts and delete if False
            if not author_has_posts:
                cursor.execute('''DELETE FROM author WHERE name = %s''', author_name)
        except Exception as ex:
            LOGGER.error(f"{ex}")
            raise ex
