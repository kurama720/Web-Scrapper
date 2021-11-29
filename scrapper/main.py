"""Main module of scrapper. Scrolls Top -> Month, saves it in to html code file. Collect author's and post's urls from
file. Parses them with BS4 and Selenium, then send POST request to API with pulled records.
"""
import uuid
import time
import datetime
from typing import List, NoReturn, Dict
import json

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from scrapper.selenium_driver import driver
from scrapper.logger import create_logger
from scrapper.handlers import exception_handler, inner_exception_handler

URL: str = 'https://www.reddit.com/top/?t=month'

LOGGER = create_logger()


def get_data(records_amount) -> NoReturn:
    """Parse reddit.com with Selenium. Take amount of records to be pulled

     Scroll until find given amount posts, then save given html code into a file reddit_source.html

    """
    scroll_time_start: float = time.time()
    LOGGER.info('Program started. To break use ctrl+C')
    try:
        # Feed driver with the URL.
        driver.get(url=URL)
        while True:
            # Scroll page until there is 100 posts on it.
            if len(driver.find_elements(By.CLASS_NAME, '_1oQyIsiPHYt6nx7VOmd1sz')) >= records_amount:
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


api_URL = 'http://127.0.0.1:8087/posts'


@exception_handler
def get_data_to_record(records_amount):
    """Parse urls given in two global lists USER_URLS_LIST and POST_URLS_LIST with both BeautifulSoup and Selenium.
    Pull all the required information and send data to API.
    """

    # Run a cycle to connect post and author's urls
    @inner_exception_handler
    def find_elements():
        c = 0
        for i in range(len(POST_URLS_LIST)):
            if c >= records_amount:
                break
            else:
                c += 1
                data_to_record: Dict[str, str] = {}
                cycle_start_time: float = time.time()
                # Create all necessary connections for parsing
                session = HTMLSession()
                driver.get(url=POST_URLS_LIST[i])
                action = ActionChains(driver)
                response_user = session.get(url=USER_URLS_LIST[i])
                soup_user = BeautifulSoup(response_user.content, 'lxml')
                # Wait until data is loaded on a page
                try:
                    WebDriverWait(driver, 20) \
                        .until(ec.presence_of_element_located((By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG')))
                    # Create an id
                    data_to_record['post_id'] = str(uuid.uuid4())
                    data_to_record['post_url'] = POST_URLS_LIST[i]
                    # Find author's username
                    data_to_record['author']: str = driver.find_element(By.CLASS_NAME,
                                                                        '_2mHuuvyV9doV3zwbZPtIPG').text[2:]
                    # Check if author's profile has 18+ limit
                    if soup_user.find('h3', text='You must be 18+ to view this community'):
                        data_to_record['user_karma']: str = '18+ profile'
                        data_to_record['cake_day']: str = '18+ profile'
                    # Check if author's profile has been suspended
                    elif soup_user.find('h3', class_='_2XKLlvmuqdor3RvVbYZfgz'):
                        data_to_record['user_karma']: str = 'Account has been suspended'
                        data_to_record['cake_day']: str = 'Account has been suspended'
                    # Then find cake day and user karma
                    else:
                        data_to_record['user_karma']: str = soup_user.find(
                            'span', id='profile--id-card--highlight-tooltip--karma').text
                        data_to_record['cake_day']: str = soup_user.find(
                            'span', id='profile--id-card--highlight-tooltip--cakeday').text
                    # Find number of comments on a post
                    data_to_record['comments_number']: str = driver.find_element(By.CLASS_NAME,
                                                                                 '_1UoeAeSRhOKSNdY_h3iS1O').text
                    # Find number of votes on a post
                    data_to_record['votes_number']: str = driver.find_element(By.CLASS_NAME,
                                                                              '_1rZYMD_4xY3gRcSS3p8ODO').text
                    # Find post category and remove the prefix r/
                    data_to_record['post_category']: str = driver.find_element(
                        By.CLASS_NAME, '_19bCWnxeTjqzBElWZfIlJb').get_property('title')[2:]
                    # Use selenium to imitate cursor freezing to load other information and wait until it loads
                    action.move_to_element(driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG')).perform()
                    WebDriverWait(driver, 20) \
                        .until(ec.presence_of_element_located((By.CLASS_NAME, '_18aX_pAQub_mu1suz4-i8j')))
                    # Find list of post and comment karma
                    post_and_comment_karma: List = driver.find_elements(By.CLASS_NAME, '_18aX_pAQub_mu1suz4-i8j')
                    data_to_record['post_karma']: str = post_and_comment_karma[0].text
                    data_to_record['comment_karma']: str = post_and_comment_karma[1].text
                    # Find post date
                    amount = []
                    for item in driver.find_element(By.CLASS_NAME, '_3jOxDPIQ0KaOWpzvSQo-1s').text:
                        if item in [str(i) for i in range(1, 10)]:
                            amount.append(item)
                    current_date = datetime.datetime.now()
                    delta = datetime.timedelta(days=(int(''.join(amount))))
                    current_date = current_date - delta
                    data_to_record['post_date'] = f"{current_date.day}-{current_date.month}-{current_date.year}"

                except TimeoutException:
                    # try to refresh the page
                    try:
                        driver.refresh()
                        WebDriverWait(driver, 20) \
                            .until(ec.presence_of_element_located((By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG')))
                    # if exception raises anyway, provide fields with "data wasn't loaded"
                    except TimeoutException:
                        data_to_record['post_id'] = str(uuid.uuid4())
                        data_to_record['post_url'] = POST_URLS_LIST[i]
                        data_to_record = {k: "null" for k in ['author', 'user_karma', 'cake_day',
                                                              'comments_number', 'votes_number',
                                                              'post_category', 'post_karma',
                                                              'comment_karma', 'post_date']}
                finally:
                    requests.post(url=api_URL, data=json.dumps(data_to_record))

                cycle_end_time: int = int(time.time() - cycle_start_time)
                if '' not in data_to_record.values():
                    LOGGER.info(f"Record number {i + 1} was pulled successfully in {cycle_end_time} sec")
                else:
                    LOGGER.warning(f"Record number {i + 1} has some unfilled fields, was pulled in {cycle_end_time}"
                                   f" sec")

    find_elements()


def main(records_amount) -> NoReturn:
    """Execute all functions needed for parsing."""
    try:
        get_data(records_amount)
        get_data_urls()
        get_data_to_record(records_amount)
    finally:
        # Close connections
        driver.close()
        driver.quit()
