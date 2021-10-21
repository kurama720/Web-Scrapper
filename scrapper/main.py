import uuid
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from selenium_driver import driver


def get_data(url):
    try:
        driver.get(url=url)
        time.sleep(3)

        post_counter = 0
        while True:
            if post_counter >= 500:
                with open('reddit_source.html', 'w', encoding='utf8') as f:
                    f.write(driver.page_source)
                break
            else:
                post_for_move_to = driver.find_element(By.CLASS_NAME, 'promotedlink')
                driver.execute_script('arguments[0].scrollIntoView(true);', post_for_move_to)
                posts = driver.find_elements(By.CLASS_NAME, '_1oQyIsiPHYt6nx7VOmd1sz')
                post_counter += len(posts)

    except EOFError as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


def record_data(file_path):
    with open(file_path) as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all('a', class_='SQnoC3ObvgnGjWt90zD9Z')

    with open('reddit-YYYYMMDDHHMM.txt', 'w') as f:
        for i in range(0, len(links)):
            f.write(f"UNIQUE_ID: {uuid.uuid4()}; URL: https://www.reddit.com/{links[i].get('href')}\n")


def main():
    get_data('https://www.reddit.com/top/?t=month')
    record_data('reddit_source.html')


if __name__ == '__main__':
    main()
