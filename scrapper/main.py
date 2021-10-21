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


def record_data(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all('a', class_='SQnoC3ObvgnGjWt90zD9Z')

    with open('reddit-YYYYMMDDHHMM.txt', 'w') as f:
        row_counter = 0
        for i in range(0, len(links)):
            if row_counter == 100:
                break
            else:
                f.write(f"UNIQUE_ID: {uuid.uuid4()}; URL: https://www.reddit.com/{links[i].get('href')}\n")
                row_counter += 1


def main():
    get_data('https://www.reddit.com/top/?t=month')
    record_data('reddit_source.html')


if __name__ == '__main__':
    main()
