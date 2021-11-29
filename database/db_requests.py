"""Module for requests to db. Inserts, finds, updates and deletes given documents.
"""

from typing import List

from database.db_connection import author_collection, posts_collection

AUTHOR_FIELDS = ['user_karma', 'cake_day', 'post_karma', 'comment_karma']
POST_FIELDS = ['_id', 'post_url', 'comments_number', 'votes_number', 'post_category', 'post_date']


def find_document(element_id: dict):
    """Search for document containing given elements in given collection. Take boolean argument all_doc, search for all
    documents in collection if True.
    """
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


def insert_document(data: dict):
    """Insert a document to db. Divide data on author data and post data, then save it into collections.
     Take data to be inserted"""
    author_data = {k: v for k, v in data.items() if k in AUTHOR_FIELDS}
    post_data = {k: v for k, v in data.items() if k in POST_FIELDS}
    author_data['_id'] = data['author']
    post_data['author_name'] = author_data['_id']
    if not author_collection.find_one({'_id': data['author']}):
        author_collection.insert_one(author_data)
    posts_collection.insert_one(post_data)


def update_document(element_id: dict, new_data: dict):
    """Update document having given id with new_values"""
    author_new_data = {k: v for k, v in new_data.items() if k in AUTHOR_FIELDS}
    post_new_data = {k: v for k, v in new_data.items() if k in POST_FIELDS}
    post_author: str = posts_collection.find_one(element_id)['author_name']
    author_collection.update_one({'_id': post_author}, {'$set': author_new_data})
    posts_collection.update_one(element_id, {'$set': post_new_data})


def delete_document(element_id):
    """Delete document with given id"""
    author_name = find_document(element_id)['author_name']
    print(author_name)
    posts_collection.delete_one(element_id)
    author_has_posts = [i for i in posts_collection.find({'author_name': author_name})]
    print(author_has_posts)
    if not author_has_posts:
        author_collection.delete_one({'_id': author_name})
