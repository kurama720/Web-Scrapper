"""Module for requests to db. Inserts, finds, updates and deletes given documents."""

from typing import List

from database.db_connection import author_collection, posts_collection
from scrapper.main import LOGGER

AUTHOR_FIELDS = ['user_karma', 'cake_day', 'post_karma', 'comment_karma']
POST_FIELDS = ['_id', 'post_url', 'comments_number', 'votes_number', 'post_category', 'post_date']


def find_document(element_id: dict):
    """Search for document containing given elements in given collection. Take boolean argument all_doc, search for all
    documents in collection if True.

    :param dict element_id: _id of post to be searched
    :return: list of documents
    """
    try:
        if not element_id:
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
            post_doc: dict = posts_collection.find_one(element_id)
            author_doc: dict = author_collection.find_one({'_id': post_doc['author_name']})
            del author_doc['_id']
            return {**post_doc, **author_doc}
    except Exception as ex:
        LOGGER.error(f"{ex}")


def insert_document(data: dict):
    """Insert a document to db. Divide data on author data and post data, then save it into collections.
     Take data to be inserted

     :param dict data: data to be inserted
     """
    try:
        author_data = {k: v for k, v in data.items() if k in AUTHOR_FIELDS}
        post_data = {k: v for k, v in data.items() if k in POST_FIELDS}
        author_data['_id'] = data['author']
        post_data['author_name'] = author_data['_id']
        if not author_collection.find_one({'_id': data['author']}):
            author_collection.insert_one(author_data)
        posts_collection.insert_one(post_data)
    except Exception as ex:
        LOGGER.error(f"{ex}")


def update_document(element_id: dict, new_data: dict):
    """Update document having given id with new_values

    :param dict element_id: post _id to be updated
    :param dict new_data: data to be updated
    """
    try:
        author_new_data = {k: v for k, v in new_data.items() if k in AUTHOR_FIELDS}
        post_new_data = {k: v for k, v in new_data.items() if k in POST_FIELDS}
        post_author: str = posts_collection.find_one(element_id)['author_name']
        author_collection.update_one({'_id': post_author}, {'$set': author_new_data})
        posts_collection.update_one(element_id, {'$set': post_new_data})
    except Exception as ex:
        LOGGER.error(f"{ex}")


def delete_document(element_id: dict):
    """Delete document with given id. Check whether author has more posts, if not delete him.

    :param dict element_id: post _id to be deleted
    """
    try:
        author_name = find_document(element_id)['author_name']
        posts_collection.delete_one(element_id)
        author_has_posts = [i for i in posts_collection.find({'author_name': author_name})]
        if not author_has_posts:
            author_collection.delete_one({'_id': author_name})
    except Exception as ex:
        LOGGER.error(f"{ex}")
