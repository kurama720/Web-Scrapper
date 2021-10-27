"""A scrapper for reddit.com. Uses BeautifulSoup and Selenium to parse. Searches for 100 posts in category Top ->
This Month. Pulls such info as: post URL, author's username, author's karma, cake day, post karma, comment karma, post
date, number of comments, number of votes and post category. And also assigns a unique id for each record with uuid.
Writes this info into a txt file named reddit-YYYY-MM-DD-HH-MM, where YYYY - year, MM - month, DD - day, HH - hour,
MM - minute. Scrapping takes ~15 minutes.

No arguments are to be given. To run the scrapper execute the function main().

"""

import uuid
import time
import datetime
from typing import List, Dict, NoReturn

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib3.exceptions import MaxRetryError

from selenium_driver import driver
from logger import create_logger


URL: str = 'https://www.reddit.com/top/?t=month'

LOGGER = create_logger()


def get_data() -> NoReturn:
    """Parse reddit.com with Selenium.

    Scroll until find 100 posts, then save given html-code into a file reddit_source.html

    """
    scroll_time_start: float = time.time()
    try:
        # Feed driver with the URL.
        driver.get(url=URL)
        while True:
            # Scroll page until there is 100 posts on it.
            if len(driver.find_elements(By.CLASS_NAME, '_1oQyIsiPHYt6nx7VOmd1sz')) == 100:
                with open('reddit_source.html', 'w', encoding='utf8') as f:
                    f.write(driver.page_source)
                break
            else:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    except Exception as ex:
        LOGGER.error(f"{ex} occurred in function get_data()")

    finally:
        scroll_time_end: float = time.time() - scroll_time_start
        LOGGER.info("Scrolling done in {0:.1f} sec".format(scroll_time_end))


USER_URLS_LIST: List[str] = []
POST_URLS_LIST: List[str] = []


def get_data_urls() -> NoReturn:
    """Parse reddit_source.html with BeautifulSoup.

    Look for post and author's urls. Save them into the global lists USER_URLS_LIST and POST_URLS_LIST.

    """
    urls_start_time: float = time.time()
    with open('reddit_source.html', 'r', encoding='utf8') as f:
        src = f.read()
    try:
        # Create connections
        soup = BeautifulSoup(src, 'lxml')
        soup_for_post_url = BeautifulSoup(src, 'lxml')
        # Parse and pull urls
        user_urls: List = soup.find_all('a', class_='_2tbHP6ZydRpjI44J3syuqC')
        post_urls: List = soup_for_post_url.find_all('a', class_='SQnoC3ObvgnGjWt90zD9Z')
        # Save them into the lists.
        global USER_URLS_LIST, POST_URLS_LIST
        USER_URLS_LIST = ['https://www.reddit.com' + item.get('href') for item in user_urls]
        POST_URLS_LIST = ['https://www.reddit.com' + item.get('href') for item in post_urls]

        urls_end_time: float = time.time() - urls_start_time
        LOGGER.info(f"Urls were successfully saved in {urls_end_time:.2f} sec")

    except Exception as ex:
        LOGGER.error(f"{ex} occurred in function get_urls()")


def get_data_to_record() -> NoReturn:
    """Parse urls given in two global lists USER_URLS_LIST and POST_URLS_LIST with both BeautifulSoup and Selenium.
    Pull all the required information and save it into the file reddit-YYYY-MM-DD-HH-MM.txt.

    Info from users' profiles having 18+ limit save as '18+ content'. If any other problem with pulling data occurs,
    save element as 'Element was not found'. Exceptions related to not finding data are caught. Not found element will
    be saved as 'Element was not found'. Exceptions related to connection mostly occur due to closing driver before
    function executed.

    """
    current_datetime = datetime.datetime.now()
    # Create appropriate file name
    file_name = 'reddit-{year}-{month}-{day}-{hour}h-{minute}m.txt'.format(
        year=current_datetime.year,
        month=current_datetime.month,
        day=current_datetime.day,
        hour=current_datetime.hour,
        minute=current_datetime.minute
    )
    with open(file_name, 'w', encoding='utf8') as f:
        start_time: float = time.time()
        # Run a cycle to connect post and author's urls
        try:
            for i in range(0, len(POST_URLS_LIST)):
                cycle_start_time: float = time.time()
                # Create all necessary connections for parsing
                session = HTMLSession()
                driver.get(url=POST_URLS_LIST[i])
                action = ActionChains(driver)
                response_user = session.get(url=USER_URLS_LIST[i])
                soup_user = BeautifulSoup(response_user.content, 'lxml')
                # Wait until info is loaded on a page
                WebDriverWait(driver, 10)\
                    .until(ec.presence_of_element_located((By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG')))
                # Find author's username
                try:
                    author: str = driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG').text\
                        .removeprefix('u/')
                except (AttributeError, NoSuchElementException):
                    author = 'Element was not found'
                    LOGGER.error(f"Element author was not found  in {i+1} record")
                except Exception as ex:
                    LOGGER.error(f"{ex} occurred with the element: author in {i+1} record")
                try:
                    # Check if author's profile has 18+ limit. Then find cake day and user karma
                    if soup_user.find('h3', text='You must be 18+ to view this community'):
                        user_karma: str = '18+ profile'
                        cake_day: str = '18+ profile'
                    else:
                        user_karma: str = soup_user.find('div', class_='_3KNaG9-PoXf4gcuy5_RCVy').text
                        cake_day: str = soup_user.find('span', id='profile--id-card--highlight-tooltip--cakeday').text
                except (AttributeError, NoSuchElementException):
                    user_karma = 'Element was not found'
                    cake_day = 'Element was not found'
                    LOGGER.error(f"Elements user_karma, cake_day were not found  in {i + 1} record")
                except Exception as ex:
                    LOGGER.error(f"{ex} occurred with the elements: user_karma, cake_day  in {i+1} record")
                try:
                    # Find number of comments on a post.
                    number_of_comments: str = driver.find_element(By.CLASS_NAME, '_1UoeAeSRhOKSNdY_h3iS1O').text
                except (AttributeError, NoSuchElementException):
                    number_of_comments = 'Element was not found'
                    LOGGER.error(f"Element number_of_comments was not found  in {i + 1} record")
                except Exception as ex:
                    LOGGER.error(f"{ex} occurred with the element: number_of_comments  in {i+1} record")
                try:
                    # Find number of votes on a post
                    number_of_votes: str = driver.find_element(By.CLASS_NAME, '_1rZYMD_4xY3gRcSS3p8ODO').text
                except (AttributeError, NoSuchElementException):
                    number_of_votes = 'Element was not found'
                    LOGGER.error(f"Element number_of_votes was not found  in {i + 1} record")
                except Exception as ex:
                    LOGGER.error(f"{ex} occurred with the element: number_of_votes  in {i+1} record")
                try:
                    # Find post category and remove the prefix r/
                    post_category: str = driver.find_element(By.CLASS_NAME, '_19bCWnxeTjqzBElWZfIlJb')\
                        .get_property('title').removeprefix('r/')
                except (AttributeError, NoSuchElementException):
                    post_category = 'Element was not found'
                    LOGGER.error(f"Element post_category was not found in {i+1} record")
                except Exception as ex:
                    LOGGER.error(f"{ex} occurred with the element: post_category in {i+1} record")
                # Use selenium to imitate cursor freezing to load other information and wait until it loads.
                action.move_to_element(driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG')).perform()
                WebDriverWait(driver, 10)\
                    .until(ec.presence_of_element_located((By.CLASS_NAME, '_18aX_pAQub_mu1suz4-i8j')))
                try:
                    # Find list of post and comment karma
                    post_and_comment_karma: List = driver.find_elements(By.CLASS_NAME, '_18aX_pAQub_mu1suz4-i8j')
                    post_karma: str = post_and_comment_karma[0].text
                    comment_karma: str = post_and_comment_karma[1].text
                except (IndexError, NoSuchElementException):
                    post_karma = 'Element was not found'
                    comment_karma = 'Element was not found'
                    LOGGER.error(f'Post and comment karma were not found in {i+1} record')
                except Exception as ex:
                    LOGGER.error(f"{ex} occurred with the elements: post_karma, comment_karma in {i+1} record")
                # Save all the info into the dictionary
                data_to_record: Dict[str, str] = {
                    'UNIQUE ID': str(uuid.uuid4()),
                    'POST URL': POST_URLS_LIST[i],
                    'AUTHOR': author,
                    'USER KARMA': user_karma,
                    'CAKE DAY': cake_day,
                    'POST KARMA': post_karma,
                    'COMMENT KARMA': comment_karma,
                    'NUMBER OF COMMENTS': number_of_comments,
                    'NUMBER OF VOTES': number_of_votes,
                    'POST CATEGORY': post_category,
                }
                # Record data into the file
                f.write(f"{data_to_record}\n")
                cycle_end_time: int = int(time.time() - cycle_start_time)
                if 'Element was not found' not in data_to_record.values():
                    LOGGER.info(f"Record number {i+1} was pulled successfully in {cycle_end_time} sec")
                else:
                    LOGGER.warning(f"Record number {i+1} has some unfilled fields, was pulled in {cycle_end_time} sec")

        except MaxRetryError:
            LOGGER.error('Problems with connection occurred')
        except IndexError:
            LOGGER.error('Url list is empty')
        except Exception as ex:
            LOGGER.error(f"{ex} occurred in function get_record_to_record()")

        finally:
            LOGGER.info(f"Recording time spent: {(time.time() - start_time)//60} min")


def main() -> NoReturn:
    """Execute all functions needed for parsing."""
    program_start: float = time.time()
    get_data()
    get_data_urls()
    get_data_to_record()
    # Close connections
    driver.close()
    driver.quit()
    LOGGER.info(f"Total time spent {(time.time() - program_start) // 60} min")


if __name__ == '__main__':
    main()
