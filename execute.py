"""Module for running program from console. Uses module argparse.
"""

import argparse

# Create a parser
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-r', '--records_amount', type=int, help='How many records to pull')
PARSER.add_argument('-a', '--action', required=True, choices=['runserver', 'runscrapper', 'file', 'rows', 'logs'],
                    help='<runserver> - to execute the program; <file> to know the file name; <rows> - to know the'
                         ' amount of records; <logs> to show logs')
args = PARSER.parse_args()
# Catch keywords from commandline.
if args.action == 'runserver':
    from api.server import main
    main()
elif args.action == 'runscrapper':
    from scrapper.main import main
    main(args.records_amount)
elif args.action == 'file':
    with open('file_info.txt', 'r') as f:
        print(f.readlines()[0])
elif args.action == 'rows':
    with open('file_info.txt', 'r') as f:
        print(f.readlines()[1])
elif args.action == 'logs':
    with open('logs.log', 'r') as f:
        print(f.read())
