import uuid
import time
import datetime
import logging

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from urllib3.exceptions import MaxRetryError

from selenium_driver import driver


URL = 'https://www.reddit.com/top/?t=month'

MAX_WAIT = 20


def create_loger():
    logger = logging.getLogger('scrapper/main.py')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler('logs.log', mode='w')
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


LOGGER = create_loger()


def get_data():
    scroll_time_start = time.time()
    try:
        driver.get(url=URL)
        post_counter = 0
        while True:
            if post_counter >= 2000:
                with open('reddit_source.html', 'w', encoding='utf8') as f:
                    f.write(driver.page_source)
                break
            else:
                post_for_move_to = driver.find_element(By.CLASS_NAME, 'promotedlink')
                driver.execute_script('arguments[0].scrollIntoView(true);', post_for_move_to)
                posts = driver.find_elements(By.CLASS_NAME, '_1oQyIsiPHYt6nx7VOmd1sz')
                post_counter += len(posts)

    except Exception as ex:
        LOGGER.error(f"{ex} occured in function get_data()")

    finally:
        scroll_time_end = time.time() - scroll_time_start
        LOGGER.info("Scrolling done in {0:.1f} sec".format(scroll_time_end))


user_urls_list = []
post_urls_list = []


def get_data_urls():
    urls_start_time = time.time()
    with open('reddit_source.html', 'r', encoding='utf8') as f:
        src = f.read()
    try:
        soup = BeautifulSoup(src, 'lxml')
        soup_for_post_url = BeautifulSoup(src, 'lxml')

        user_urls = soup.find_all('a', class_='_2tbHP6ZydRpjI44J3syuqC')
        post_urls = soup_for_post_url.find_all('a', class_='SQnoC3ObvgnGjWt90zD9Z')

        for item in user_urls:
            if len(user_urls_list) == 100:
                break
            else:
                user_url = 'https://www.reddit.com' + item.get('href')
                user_urls_list.append(user_url)

        for item in post_urls:
            if len(post_urls_list) == 100:
                break
            else:
                post_url = 'https://www.reddit.com' + item.get('href')
                post_urls_list.append(post_url)

        urls_end_time = time.time() - urls_start_time
        LOGGER.info(f"Urls were successfully saved in {urls_end_time:.2f} sec")

    except Exception as ex:
        LOGGER.error(f"{ex} occured in function get_urls()")


def get_data_to_record():
    current_datetime = datetime.datetime.now()
    file_name = 'reddit-{year}-{month}-{day}-{hour}h-{minute}m.txt'.format(
        year=current_datetime.year,
        month=current_datetime.month,
        day=current_datetime.day,
        hour=current_datetime.hour,
        minute=current_datetime.minute
    )
    with open(file_name, 'w', encoding='utf8') as f:
        start_time = time.time()
        try:
            for i in range(0, len(post_urls_list)):
                cycle_start_time = time.time()
                session = HTMLSession()
                driver.get(url=post_urls_list[i])
                action = ActionChains(driver)
                response_user = session.get(url=user_urls_list[i])
                soup_user = BeautifulSoup(response_user.content, 'lxml')

                unique_id = uuid.uuid4()
                post_url = post_urls_list[i]
                try:
                    author = driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG').text\
                        .removeprefix('u/')
                except AttributeError:
                    author = 'Element was not found'
                except NoSuchElementException:
                    LOGGER.error(f"Element {author} was not found")
                except Exception as ex:
                    LOGGER.error(f"{ex} occured with the element: {author}")
                try:
                    if soup_user.find('h3', text='You must be 18+ to view this community'):
                        user_karma = '18+ profile'
                    else:
                        user_karma = soup_user.find('div', class_='_3KNaG9-PoXf4gcuy5_RCVy').text
                except AttributeError:
                    user_karma = 'Element was not found'
                except NoSuchElementException:
                    LOGGER.error(f"Element {author} was not found")
                except Exception as ex:
                    LOGGER.error(f"{ex} occured with the element: {user_karma}")
                try:
                    if soup_user.find('h3', text='You must be 18+ to view this community'):
                        cake_day = '18+ profile'
                    else:
                        cake_day = soup_user.find('span', id='profile--id-card--highlight-tooltip--cakeday').text
                except AttributeError:
                    cake_day = 'Element was not found'
                except NoSuchElementException:
                    LOGGER.error(f"Element {author} was not found")
                except Exception as ex:
                    LOGGER.error(f"{ex} occured with the element: {cake_day}")
                try:
                    number_of_comments = driver.find_element(By.CLASS_NAME, '_1UoeAeSRhOKSNdY_h3iS1O').text
                except AttributeError:
                    number_of_comments = 'Element was not found'
                except NoSuchElementException:
                    LOGGER.error(f"Element {author} was not found")
                except Exception as ex:
                    LOGGER.error(f"{ex} occured with the element: {number_of_comments}")
                try:
                    number_of_votes = driver.find_element(By.CLASS_NAME, '_1rZYMD_4xY3gRcSS3p8ODO').text
                except AttributeError:
                    number_of_votes = 'Element was not found'
                except NoSuchElementException:
                    LOGGER.error(f"Element {author} was not found")
                except Exception as ex:
                    LOGGER.error(f"{ex} occured with the element: {number_of_votes}")
                try:
                    post_category = driver.find_element(By.CLASS_NAME, '_2Zdkj7cQEO3zSGHGK2XnZv').text\
                                    .removeprefix('r/')
                except AttributeError:
                    post_category = 'Element was not found'
                except NoSuchElementException:
                    LOGGER.error(f"Element {author} was not found")
                except Exception as ex:
                    LOGGER.error(f"{ex} occured with the elements : {post_karma, comment_karma}")
                action.move_to_element(driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPt'
                                                                          'IPG')).perform()
                time.sleep(2)
                try:
                    post_and_comment_karma = driver.find_elements(By.CLASS_NAME, '_18aX_pAQub_mu1suz4-i8j')
                    post_karma = post_and_comment_karma[0].text
                    comment_karma = post_and_comment_karma[1].text
                except IndexError:
                    post_karma = 'Element was not found'
                    comment_karma = 'Element was not found'
                    LOGGER.error('Post and comment karma were not found, probably because of being not loaded')
                except NoSuchElementException:
                    LOGGER.error(f"Element {author} was not found")
                except Exception as ex:
                    LOGGER.error(f"{ex} occured with the element:{post_karma, comment_karma}")
                data_to_record = {
                    'UNIQUE ID': unique_id,
                    'POST URL': post_url,
                    'AUTHOR': author,
                    'USER KARMA': user_karma,
                    'CAKE DAY': cake_day,
                    'POST KARMA': post_karma,
                    'COMMENT KARMA': comment_karma,
                    'NUMBER OF COMMENTS': number_of_comments,
                    'NUMBER OF VOTES': number_of_votes,
                    'POST CATEGORY': post_category,
                }
                f.write(f"{data_to_record}\n")
                cycle_end_time = int(time.time() - cycle_start_time)
                if 'Element was not found' not in data_to_record.values():
                    LOGGER.info(f"Record number {i+1} was pulled successfully in {cycle_end_time} sec")
                else:
                    LOGGER.warning(f"Record number {i+1} has some unfilled fields, was pulled in {cycle_end_time} sec")

        except MaxRetryError:
            LOGGER.error('Problems with connection occured')
        except IndexError:
            LOGGER.error('Url list is empty')
        except Exception as ex:
            LOGGER.error(f"{ex}")

        finally:
            LOGGER.info(f"Recording time spent: {(time.time() - start_time)//60} min")


def main():
    programm_start = time.time()
    get_data()
    get_data_urls()
    get_data_to_record()
    LOGGER.info(f"Total time spent {(time.time() - programm_start) // 60} min")


if __name__ == '__main__':
    main()
