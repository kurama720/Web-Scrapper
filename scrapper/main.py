import uuid
import time
from urllib3.exceptions import MaxRetryError

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

from selenium_driver import driver


URL = 'https://www.reddit.com/top/?t=month'


def get_data():
    try:
        driver.get(url=URL)

        post_counter = 0
        while True:
            if post_counter >= 600:
                with open('reddit_source.html', 'w', encoding='utf8') as f:
                    f.write(driver.page_source)
                break
            else:
                post_for_move_to = driver.find_element(By.CLASS_NAME, 'promotedlink')
                driver.execute_script('arguments[0].scrollIntoView(true);', post_for_move_to)
                time.sleep(1)
                posts = driver.find_elements(By.CLASS_NAME, '_1oQyIsiPHYt6nx7VOmd1sz')
                post_counter += len(posts)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


user_urls_list = []
post_urls_list = []


def get_data_urls():
    with open('reddit_source.html', 'r', encoding='utf8') as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    soup_for_post_url = BeautifulSoup(src, 'lxml')

    item_urls = soup.find_all('a', class_='_2tbHP6ZydRpjI44J3syuqC')
    post_urls = soup_for_post_url.find_all('a', class_='SQnoC3ObvgnGjWt90zD9Z')

    for item in post_urls:
        if len(post_urls_list) == 100:
            break
        else:
            post_url = 'https://www.reddit.com' + item.get('href')
            post_urls_list.append(post_url)

    for item in item_urls:
        if len(user_urls_list) == 100:
            break
        else:
            user_url = 'https://www.reddit.com' + item.get('href')
            user_urls_list.append(user_url)


MAX_WAIT = 10


def get_data_to_record():
    with open('reddit.txt', 'w', encoding='utf8') as f:
        start_time = time.time()
        while True:
            try:
                for i in range(0, len(post_urls_list)):
                    session = HTMLSession()
                    driver.get(url=post_urls_list[i])
                    action = ActionChains(driver)
                    response_user = session.get(url=user_urls_list[i])
                    soup_user = BeautifulSoup(response_user.content, 'lxml')
                    response_post = session.get(url=post_urls_list[i])
                    soup_post = BeautifulSoup(response_post.content, 'lxml')

                    unique_id = uuid.uuid4()
                    post_url = post_urls_list[i]
                    author = driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG')
                    user_karma = soup_user.find('div', class_='_3KNaG9-PoXf4gcuy5_RCVy')
                    cake_day = soup_user.find('span', id='profile--id-card--highlight-tooltip--cakeday')
                    number_of_comments = soup_post.find('a', class_='_1UoeAeSRhOKSNdY_h3iS1O')
                    number_of_votes = soup_post.find('div', class_='_1rZYMD_4xY3gRcSS3p8ODO')
                    post_category = soup_post.find('div', class_='_2Zdkj7cQEO3zSGHGK2XnZv')

                    if author:
                        action.move_to_element(author).perform()
                        post_and_comment_karma = driver.find_elements(By.CLASS_NAME, '_18aX_pAQub_mu1suz4-i8j')
                        if post_and_comment_karma:
                            data_to_record = {
                                'UNIQUE ID': unique_id,
                                'POST URL': post_url,
                                'AUTHOR': 'No such element' if author is None else author.text.removeprefix('u/'),
                                'USER KARMA': '18+ content' if user_karma is None else user_karma.text,
                                'CAKE DAY': '18+ content' if cake_day is None else cake_day.text,
                                'POST KARMA': 'No such element' if post_and_comment_karma[0] is None
                                else post_and_comment_karma[0].text,
                                'COMMENT KARMA': 'No such element' if post_and_comment_karma[1] is None
                                else post_and_comment_karma[1].text,
                                'NUMBER OF COMMENTS': 'No such element' if number_of_comments is None
                                else number_of_comments.text,
                                'NUMBER OF VOTES': 'No such element' if number_of_votes is None
                                else number_of_votes.text,
                                'POST CATEGORY': 'No such element' if post_category is None
                                else post_category.text.removeprefix('r/'),
                            }
                            f.write(f"{data_to_record}\n")

            except (WebDriverException, MaxRetryError) as ex:
                if time.time() - start_time > MAX_WAIT:
                    raise ex
                time.sleep(0.5)
            finally:
                driver.close()
                driver.quit()


def main():
    # get_data()
    get_data_urls()
    get_data_to_record()


if __name__ == '__main__':
    main()
