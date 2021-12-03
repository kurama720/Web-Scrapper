"""Module for requests to db. Inserts, finds, updates and deletes given documents."""

from typing import List

from pymongo.errors import DuplicateKeyError

from database.db_mongo.db_connection import author_collection, posts_collection
from scrapper.logger import create_db_logger

LOGGER = create_db_logger()

AUTHOR_FIELDS = ['user_karma', 'cake_day', 'post_karma', 'comment_karma']
POST_FIELDS = ['_id', 'post_url', 'comments_number', 'votes_number', 'post_category', 'post_date']


def find_record(element_id: str = None):
    """Search for document containing given elements in given collection. Take boolean argument all_doc, search for all
    documents in collection if True.

    :param str element_id: post _id to be searched
    :return: list of documents
    """
    try:
        if element_id is None:
            author_id: List[dict] = []
            merged_docs: List[dict] = []
            for author in author_collection.find({}):
                author_id.append(author)
            for item in author_id:
                post_doc: List[dict] = [i for i in posts_collection.find({'author_name': item['_id']})]
                del item['_id']
                for doc in post_doc:
                    merged = {**doc, **item}
                    merged_docs.append(merged)
            return merged_docs
        else:
            post_doc: dict = posts_collection.find_one({'_id': element_id})
            author_doc: dict = author_collection.find_one({'_id': post_doc['author_name']})
            del author_doc['_id']
            return {**post_doc, **author_doc}
    except TypeError:
        raise TypeError
    except Exception as ex:
        LOGGER.error(f"{ex}")
        raise ex


def insert_record(data: dict):
    """Insert a document to db. Divide data on author data and post data, then save it into collections.
     Take data to be inserted

     :param dict data: data to be inserted
     """
    try:
        author_data = {k: v for k, v in data.items() if k in AUTHOR_FIELDS}
        post_data = {k: v for k, v in data.items() if k in POST_FIELDS}
        author_data['_id'] = data['author']
        post_data['author_name'] = author_data['_id']
        author_exists = author_collection.find_one({'_id': data['author']})
        if not author_exists:
            author_collection.insert_one(author_data)
        posts_collection.insert_one(post_data)
    except DuplicateKeyError:
        raise DuplicateKeyError
    except Exception as ex:
        LOGGER.error(f"{ex}")
        raise ex


def update_record(element_id: str, new_data: dict):
    """Update document having given id with new_values

    :param dict element_id: post _id to be updated
    :param dict new_data: data to be updated
    """
    try:
        author_new_data = {k: v for k, v in new_data.items() if k in AUTHOR_FIELDS}
        post_new_data = {k: v for k, v in new_data.items() if k in POST_FIELDS}
        post_author: str = posts_collection.find_one({'_id': element_id})['author_name']
        author_collection.update_one({'_id': post_author}, {'$set': author_new_data})
        posts_collection.update_one({'_id': element_id}, {'$set': post_new_data})
    except TypeError:
        raise TypeError
    except Exception as ex:
        LOGGER.error(f"{ex}")
        raise ex


def delete_record(element_id: str):
    """Delete document with given id. Check whether author has more posts, if not delete him.

    :param dict element_id: post _id to be deleted
    """
    try:
        author_name = find_record(element_id)['author_name']
        posts_collection.delete_one({'_id': element_id})
        author_has_posts = [i for i in posts_collection.find({'author_name': author_name})]
        if not author_has_posts:
            author_collection.delete_one({'_id': author_name})
    except TypeError:
        raise TypeError
    except Exception as ex:
        LOGGER.error(f"{ex}")
        raise ex
