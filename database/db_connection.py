"""Creates connection to Mongo and collection named <posts>.
"""

import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['PostsDB']

posts_collection = db['posts']
