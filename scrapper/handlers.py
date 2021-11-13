"""Creates exception handling decorators"""

import time
from urllib3.exceptions import MaxRetryError

from selenium.common.exceptions import NoSuchElementException, WebDriverException

from scrapper.logger import logger_for_handlers

LOGGER_HANDLER = logger_for_handlers()


# Exception handler for get_data_to_record() func
def exception_handler(func):
    def wrapper(*args, **kwargs):
        start_time: float = time.time()
        try:
            func(*args, **kwargs)
        except MaxRetryError:
            LOGGER_HANDLER.error('Problems with connection occurred')
        except IndexError:
            LOGGER_HANDLER.error('Url list is empty')
        except Exception as ex:
            LOGGER_HANDLER.error(f"{ex} occurred in function get_record_to_record()")
        finally:
            LOGGER_HANDLER.info(f"Recording time spent: {(time.time() - start_time) // 60} min")
    return wrapper


# Exception handler for inner find_elements() func
def inner_exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (AttributeError, NoSuchElementException):
            LOGGER_HANDLER.error(f"Some elements were not found in a record")
        except WebDriverException as ex:
            LOGGER_HANDLER.error(f"{ex} occurred in a record")
        except Exception as ex:
            LOGGER_HANDLER.error(f"{ex} occurred in a record")
    return wrapper
