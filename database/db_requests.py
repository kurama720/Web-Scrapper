"""Module for requests to db. Inserts, finds, updates and deletes given documents.
"""


def insert_document(collection, data):
    """Insert a document to db. Take data to be inserted and collection which is inserted to"""
    collection.insert_one(data)


def find_document(collection, elements, all_doc=False):
    """Search for document containing given elements in given collection. Take boolean argument all_doc, search for all
    documents in collection if True
    """
    if all_doc:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def update_document(collection, element_id, new_values):
    """Update document having given id with new_values"""
    collection.update_one(element_id, {'$set': new_values})


def delete_document(collection, element_id):
    """Delete document with given id"""
    collection.delete_one(element_id)
