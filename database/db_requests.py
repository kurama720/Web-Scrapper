"""Module implements processing requests to database. """
from database.db_connection import create_connection

CONNECTION = create_connection()
CURSOR = CONNECTION.cursor()


def insert_record(data: dict):
    """Insert records in database"""
    save_record = '''INSERT INTO post (post_url, author, user_karma, cake_day, comments_number, votes_number,
                   post_category, post_karma, comment_karma, post_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   '''
    CURSOR.execute(save_record, ([i for i in data.values()]))


def find_record(element_id: str = 0, all_records=False):
    """Find records in database, If all_records True then find all of records. Provide taken data with fields and
    return dict"""
    fields = ['UNIQUE ID', 'POST URL', 'AUTHOR', 'USER KARMA', 'CAKE DAY', 'COMMENTS NUMBER', 'VOTES_NUMBER',
              'POST CATEGORY', 'POST KARMA', 'COMMENT KARMA', 'POST DATE']
    if all_records:
        find_all = '''SELECT * from post'''
        CURSOR.execute(find_all)
        data = CURSOR.fetchall()
        output = []
        for data in data:
            named_records = {}
            for i in range(len(fields)):
                named_records[fields[i]] = data[i]
            output.append(named_records)
        return output
    else:
        find_by_id = '''SELECT * from post WHERE post_id = %s'''
        CURSOR.execute(find_by_id, (element_id,))
        data = CURSOR.fetchall()
        for data in data:
            named_records = {}
            for i in range(len(fields)):
                named_records[fields[i]] = data[i]
            return named_records


def update_record(element_id: str, data: dict):
    """Update record with given id and given data. SQL is picky, so every key is to be processed in separate block"""
    for k, v in data.items():
        if 'post_url' in k:
            update_by_id = '''UPDATE post SET post_url = %s WHERE post_id = %s'''
            CURSOR.execute(update_by_id, (v, element_id,))
        elif 'author' in k:
            update_by_id = '''UPDATE post SET author = %s WHERE post_id = %s'''
            CURSOR.execute(update_by_id, (v, element_id,))
        elif 'user_karma' in k:
            update_by_id = '''UPDATE post SET user_karma = %s WHERE post_id = %s'''
            CURSOR.execute(update_by_id, (v, element_id,))
        elif 'cake_day' in k:
            update_by_id = '''UPDATE post SET cake_day = %s WHERE post_id = %s'''
            CURSOR.execute(update_by_id, (v, element_id,))
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
            update_by_id = '''UPDATE post SET post_karma = %s WHERE post_id = %s'''
            CURSOR.execute(update_by_id, (v, element_id,))
        elif 'comment_karma' in k:
            update_by_id = '''UPDATE post SET comment_karma = %s WHERE post_id = %s'''
            CURSOR.execute(update_by_id, (v, element_id,))
        elif 'post_date' in k:
            update_by_id = '''UPDATE post SET post_date = %s WHERE post_id = %s'''
            CURSOR.execute(update_by_id, (v, element_id,))


def delete_record(element_id: str):
    """Delete record with given id"""
    delete_by_id = '''DELETE FROM post WHERE post_id = %s'''
    CURSOR.execute(delete_by_id, (element_id,))
