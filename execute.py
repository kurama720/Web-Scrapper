"""Module for running program from console. Uses module argparse."""

import argparse

# Create a parser
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-r', '--records_amount', type=int, help='How many records to pull', default=100)
PARSER.add_argument('-a', '--action', required=True, choices=['runserver', 'runscrapper', 'createvault', 'logs'],
                    help='<runserver> - to run the server; <runscrapper> - to run the scrapper; <createvault> - to'
                         'create database and table')
PARSER.add_argument('-d', '--database', default='mongo', choices=['mongo', 'postgre'],
                    help='<mongo> - to run server working on mongo; <postgre> - to run server working on postgre')
args = PARSER.parse_args()
# Catch keywords from commandline.
if args.action == 'runserver':
    if args.database == 'mongo':
        from api.select_db import select_mongo
        select_mongo()
    elif args.database == 'postgre':
        from api.select_db import select_postgre
        select_postgre()
    from api.server import run_server
    run_server()
elif args.action == 'runscrapper':
    from scrapper.main import run_scrapper
    run_scrapper(args.records_amount)
elif args.action == 'createvault':
    from database.postgre.db_connection import create_vault
    create_vault()
