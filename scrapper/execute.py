"""Module for working from console. Uses standard module argparse.

"""

import argparse

# Create a parser
PARSER = argparse.ArgumentParser(description='Executing the scrapper')
PARSER.add_argument('-a', '--action',
                    help='"run" - to execute the program; "file" to know the file name";'
                         ' "rows" - to know the amount of records')
ARGS = PARSER.parse_args()
# Catch keywords from commandline.
if ARGS.action == 'run':
    from main import main
    main()
elif ARGS.action == 'file':
    with open('file_info.txt', 'r') as f:
        print(f.readlines()[0])
elif ARGS.action == 'rows':
    with open('file_info.txt', 'r') as f:
        print(f.readlines()[1])
elif ARGS.action == 'logs':
    with open('logs.log', 'r') as f:
        print(f.read())
