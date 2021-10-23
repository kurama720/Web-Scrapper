import uuid
import time

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from selenium_driver import driver


URL = 'https://www.reddit.com/top/?t=month'


def get_data():
    try:
        driver.get(url=URL)
        time.sleep(3)

        post_counter = 0
        while True:
            if post_counter >= 2000:
                with open('reddit_source.html', 'w', encoding='utf8') as f:
                    f.write(driver.page_source)
                break
            else:
                post_for_move_to = driver.find_element(By.CLASS_NAME, 'promotedlink')
                driver.execute_script('arguments[0].scrollIntoView(true);', post_for_move_to)
                time.sleep(1)
                posts = driver.find_elements(By.CLASS_NAME, '_1oQyIsiPHYt6nx7VOmd1sz')
                post_counter += len(posts)

    except EOFError as ex:
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


def get_data_to_record():
    with open('reddit.txt', 'w', encoding='utf8') as f:
        for i in range(0, len(post_urls_list)):
            session = HTMLSession()
            response = session.get(url=user_urls_list[i])
            soup = BeautifulSoup(response.content, 'lxml')
            response_post = session.get(url=post_urls_list[i])
            soup_post = BeautifulSoup(response_post.content, 'lxml')
            try:
                unique_id = uuid.uuid4()
                post_url = post_urls_list[i]
                author = None
                user_karma = soup.find('div', class_='_3KNaG9-PoXf4gcuy5_RCVy')
                cake_day = soup.find('span', id='profile--id-card--highlight-tooltip--cakeday')
                number_of_comments = soup_post.find('a', class_='_1UoeAeSRhOKSNdY_h3iS1O')
                number_of_votes = soup_post.find('div', class_='_1rZYMD_4xY3gRcSS3p8ODO')
                data_to_record = {
                    'UNIQUE ID': unique_id,
                    'POST URL': post_url,
                    'AUTHOR': author,
                    'USER KARMA': None if user_karma is None else user_karma.text,
                    'CAKE DAY': None if cake_day is None else cake_day.text,
                    'NUMBER OF COMMENTS': None if number_of_comments is None else number_of_comments.text,
                    'NUMBER OF VOTES': None if number_of_votes is None else number_of_votes.text,
                }
                f.write(f"{data_to_record}\n")
            except EOFError as ex:
                print(ex)


def main():
    get_data()
    get_data_urls()
    get_data_to_record()


if __name__ == '__main__':
    main()

