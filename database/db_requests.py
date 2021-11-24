"""Module implements processing requests to database. """
from database.db_connection import create_connection

CONNECTION = create_connection()
CURSOR = CONNECTION.cursor()


def insert_record(data: dict):
    """Insert records in database"""
    save_author_data = '''INSERT INTO author (name, user_karma, cake_day, post_karma, comment_karma) VALUES
                          (%s, %s, %s, %s, %s)
                       '''
    save_post_data = '''INSERT INTO post (post_url, comments_number, votes_number, post_category, post_date, author_name)
     VALUES (%s, %s, %s, %s, %s, %s) 
                     '''
    author_fields = ["AUTHOR", "USER KARMA", "CAKE DAY", "POST KARMA", "COMMENT KARMA"]
    post_fields = ['POST URL', 'COMMENTS NUMBER', 'VOTES NUMBER', 'POST CATEGORY', 'POST DATE']
    author_exists = '''SELECT * from author WHERE name = %s'''
    CURSOR.execute(author_exists, (data['AUTHOR'],))
    post_data = [v for k, v in data.items() if k in post_fields]
    post_data.append(data['AUTHOR'])
    if not CURSOR.fetchall():
        CURSOR.execute(save_author_data, ([v for k, v in data.items() if k in author_fields]))
    CURSOR.execute(save_post_data, ([i for i in post_data]))


def find_record(element_id: str = '', all_records=False):
    """Find records in database, If all_records True then find all of records. Provide taken data with fields and
    return dict"""
    fields = ['UNIQUE ID', 'POST URL', 'COMMENTS NUMBER', 'VOTES_NUMBER', 'POST CATEGORY', 'POST DATE',
              'AUTHOR', 'USER KARMA', 'CAKE DAY', 'POST KARMA', 'COMMENT KARMA']
    if all_records:
        find_all = '''SELECT post_id, post_url, comments_number, votes_number, post_category, post_date, name,
                   user_karma, cake_day, post_karma, comment_karma FROM post INNER JOIN author 
                   ON post.author_name = author.name
                   '''
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
        find_by_id = '''SELECT post_id, post_url, comments_number, votes_number, post_category, post_date, name,
                   user_karma, cake_day, post_karma, comment_karma FROM post INNER JOIN author 
                   ON post.author_name = author.name WHERE post_id = %s'''
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


def delete_record(element_id: str):
    """Delete record with given id"""
    delete_by_id = '''DELETE FROM post WHERE post_id = %s'''
    CURSOR.execute(delete_by_id, (element_id,))
