"""Module for selecting database given as parameter in argparse"""

# List collecting methods from selected database
METHODS_LIST = []


def select_mongo():
    """Import package mongo and append METHODS_LIST with methods from the package"""
    from database import mongo
    METHODS_LIST.append(mongo.insert_record)
    METHODS_LIST.append(mongo.find_record)
    METHODS_LIST.append(mongo.update_record)
    METHODS_LIST.append(mongo.delete_record)


def select_postgre():
    """Import package mongo and append METHODS_LIST with methods from the package"""
    from database import postgre
    METHODS_LIST.append(postgre.insert_record)
    METHODS_LIST.append(postgre.find_record)
    METHODS_LIST.append(postgre.update_record)
    METHODS_LIST.append(postgre.delete_record)
