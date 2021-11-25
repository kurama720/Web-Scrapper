"""Module for requests to db. Inserts, finds, updates and deletes given documents.
"""

from uuid import uuid4

from database.db_connection import author_collection, posts_collection

AUTHOR_FIELDS = ['USER KARMA', 'CAKE DAY', 'POST KARMA', 'COMMENT KARMA']
POST_FIELDS = ['POST URL', 'COMMENTS NUMBER', 'VOTES NUMBER', 'POST CATEGORY', 'POST DATE']


def find_document(elements, all_doc=False):
    """Search for document containing given elements in given collection. Take boolean argument all_doc, search for all
    documents in collection if True.
    """
    if not posts_collection.find_one(elements):
        return False
    else:
        if all_doc:
            author_id = []
            merged_docs = []
            for author in author_collection.find({}):
                author_id.append(author['_id'])
            for i in author_id:
                post_doc = [i for i in posts_collection.find({'AUTHOR NAME': i})]
                author_doc = author_collection.find_one({'_id': i})
                del author_doc['_id']
                for doc in post_doc:
                    merged = {**doc, **author_doc}
                    merged_docs.append(merged)
            return merged_docs
        else:
            post_doc = posts_collection.find_one(elements)
            author_doc = author_collection.find_one({'_id': post_doc['AUTHOR NAME']})
            del author_doc['_id']
            return {**post_doc, **author_doc}


def insert_document(data):
    """Insert a document to db. Divide data on author data and post data, then save it into collections.
     Take data to be inserted"""
    author_data = {k: v for k, v in data.items() if k in AUTHOR_FIELDS}
    post_data = {k: v for k, v in data.items() if k in POST_FIELDS}
    author_data['_id'] = data['AUTHOR']
    post_data['_id'] = str(uuid4())
    post_data['AUTHOR NAME'] = author_data['_id']
    if not author_collection.find_one({'_id': data['AUTHOR']}):
        author_collection.insert_one(author_data)
    posts_collection.insert_one(post_data)


def update_document(element_id, new_data):
    """Update document having given id with new_values"""
    author_new_data = {k: v for k, v in new_data.items() if k in AUTHOR_FIELDS}
    post_new_data = {k: v for k, v in new_data.items() if k in POST_FIELDS}
    post_author = posts_collection.find_one(element_id)['AUTHOR NAME']
    author_collection.update_one({'_id': post_author}, {'$set': author_new_data})
    posts_collection.update_one(element_id, {'$set': post_new_data})


def delete_document(element_id):
    """Delete document with given id"""
    posts_collection.delete_one(element_id)
