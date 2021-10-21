import uuid
import time

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from selenium_driver import driver


def get_data(url):
    try:
        driver.get(url=url)
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

    item_urls = soup.find_all('a', class_='_2tbHP6ZydRpjI44J3syuqC') # link for user profile
    post_urls = soup_for_post_url.find_all('a', class_='SQnoC3ObvgnGjWt90zD9Z')

    for item in post_urls:
        if len(post_urls_list) == 100:
            break
        else:
            post_url = 'https://www.reddit.com/' + item.get('href')
            post_urls_list.append(post_url)

    for item in item_urls:
        if len(user_urls_list) == 100:
            break
        else:
            user_url = 'https://www.reddit.com/' + item.get('href')
            user_urls_list.append(user_url)


def get_data_to_record():
    with open('reddit.txt', 'w', encoding='utf8') as f:
        for i in range(0, len(post_urls_list)):
            response = requests.get(url=user_urls_list[i])
            soup = BeautifulSoup(response.text, 'lxml')

            try:
                data_to_record = {
                    'UNIQUE ID': uuid.uuid4(),
                    'post URL': post_urls_list[i],
                    'author': soup.find('span', class_='_1LCAhi_8JjayVo7pJ0KIh0').text,
                    'user karma': soup.find('span', id='profile--id-card--highlight-tooltip--karma').text,
                    'cake day': soup.find('span', id='profile--id-card--highlight-tooltip--cakeday').text,
                }
                f.write(f"{data_to_record}\n")
            except Exception as ex:
                print(ex)


def main():
    get_data('https://www.reddit.com/top/?t=month')
    get_data_urls()
    get_data_to_record()


if __name__ == '__main__':
    main()
