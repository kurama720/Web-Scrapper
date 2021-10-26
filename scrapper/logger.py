"""Creates logger. Saves logs into a file named logs.log"""

import logging


def create_logger():
    # Create logger
    logger = logging.getLogger('scrapper/main.py')
    logger.setLevel(logging.INFO)
    # Create a handler and a formatter for logger
    fh = logging.FileHandler('logs.log', mode='w')
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    # Add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
