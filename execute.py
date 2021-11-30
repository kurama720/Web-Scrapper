"""Module for working from console. Uses standard module argparse.
"""

import argparse

# Create a parser
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-r', '--records_amount', type=int, help='How many records to pull', default=100)
PARSER.add_argument('-a', '--action', required=True, choices=['runserver', 'runscrapper', 'createvault', 'logs'],
                    help='<runserver> - to run the server; <runscrapper> - to run the scrapper; <createvault> - to'
                         'create database and table')
args = PARSER.parse_args()
# Catch keywords from commandline.
if args.action == 'runserver':
    from api.server import run_server
    run_server()
elif args.action == 'runscrapper':
    from scrapper.main import main
    main(args.records_amount)
elif args.action == 'createvault':
    from database.db_connection import create_vault
    create_vault()
