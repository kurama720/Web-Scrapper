"""Module for working from console. Uses standard module argparse.
"""

import argparse

# Create a parser
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-r', '--records_amount', type=int, help='How many records to pull', default=100)
PARSER.add_argument('-a', '--action', required=True, choices=['runserver', 'runscrapper', 'file', 'rows', 'logs'],
                    help='<runserver> - to run the server; <runscrapper> - to run the scrapper')
args = PARSER.parse_args()
# Catch keywords from commandline.
if args.action == 'runserver':
    from api.server import main
    main()
elif args.action == 'runscrapper':
    from scrapper.main import main
    main(args.records_amount)
