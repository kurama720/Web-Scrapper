"""Creates logger. Saves logs into a file named logs.log"""

import logging


def create_logger():
    # Create logger
    logger = logging.getLogger('scrapper/main.py')
    logger.setLevel(logging.INFO)
    # Create handlers and a formatter for logger
    fh = logging.FileHandler('logs.log', mode='w')
    fh_console = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    # Add handlers and formatter to logger
    fh.setFormatter(formatter)
    fh_console.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(fh_console)
    return logger


def create_handler_logger():
    # Create logger
    logger = logging.getLogger('scrapper/handlers.py')
    logger.setLevel(logging.INFO)
    # Create handlers and a formatter for logger
    fh = logging.FileHandler('logs.log', mode='w')
    fh_console = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    # Add handlers and formatter to logger
    fh.setFormatter(formatter)
    fh_console.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(fh_console)
    return logger


def create_db_logger():
    logger = logging.getLogger('database/db_requests.py')
    logger.setLevel(logging.INFO)
    # Create handlers and a formatter for logger
    fh = logging.FileHandler('logs.log', mode='w')
    fh_console = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    # Add handlers and formatter to logger
    fh.setFormatter(formatter)
    fh_console.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(fh_console)
    return logger


def create_server_logger():
    logger = logging.getLogger('api/server.py')
    logger.setLevel(logging.INFO)
    # Create handlers and a formatter for logger
    fh = logging.FileHandler('logs.log', mode='w')
    fh_console = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    # Add handlers and formatter to logger
    fh.setFormatter(formatter)
    fh_console.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(fh_console)
    return logger
