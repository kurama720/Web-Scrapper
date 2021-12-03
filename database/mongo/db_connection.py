"""Creates connection to Mongo and collection named <posts>."""

import pymongo

DB_HOST = 'localhost'
DB_PORT = 27017

client = pymongo.MongoClient(DB_HOST, DB_PORT)
db = client['PostsDB']

posts_collection = db['post']
author_collection = db['author']
