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
                time.sleep(1)
                posts = driver.find_elements(By.CLASS_NAME, '_1oQyIsiPHYt6nx7VOmd1sz')
                post_counter += len(posts)

    except Exception as ex:
        print(ex)

    finally:
        print(f"Scrolling done in {time.time() - scroll_time_start} sec")
        driver.close()
        driver.quit()


user_urls_list = []
post_urls_list = []


def get_data_urls():
    urls_start_time = time.time()
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
    print(f"Urls were saved in {time.time() - urls_start_time} sec")


MAX_WAIT = 10


def get_data_to_record():
    with open('reddit.txt', 'w', encoding='utf8') as f:
        start_time = time.time()
        while True:
            try:
                for i in range(0, len(post_urls_list)):
                    cycle_start_time = time.time()
                    session = HTMLSession()
                    driver.get(url=post_urls_list[i])
                    action = ActionChains(driver)
                    response_user = session.get(url=user_urls_list[i])
                    soup_user = BeautifulSoup(response_user.content, 'lxml')
                    time.sleep(2)

                    unique_id = uuid.uuid4()
                    post_url = post_urls_list[i]
                    while not driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG'):
                        time.sleep(0.5)
                    else:
                        try:
                            author = driver.find_element(By.CLASS_NAME, '_2mHuuvyV9doV3zwbZPtIPG').text\
                                .removeprefix('u/')
                        except Exception as ex:
                            author = ex
                        try:
                            user_karma = soup_user.find('div', class_='_3KNaG9-PoXf4gcuy5_RCVy').text
                        except Exception as ex:
                            user_karma = ex
                        try:
                            cake_day = soup_user.find('span', id='profile--id-card--highlight-tooltip--cakeday').text
                        except Exception as ex:
                            cake_day = ex
                        try:
                            number_of_comments = driver.find_element(By.CLASS_NAME, '_1UoeAeSRhOKSNdY_h3iS1O').text
                        except Exception as ex:
                            number_of_comments = ex
                        try:
                            number_of_votes = driver.find_element(By.CLASS_NAME, '_1rZYMD_4xY3gRcSS3p8ODO').text
                        except Exception as ex:
                            number_of_votes = ex
                        try:
                            post_category = driver.find_element(By.CLASS_NAME, '_2Zdkj7cQEO3zSGHGK2XnZv').text\
                                            .removeprefix('r/')
                        except Exception as ex:
                            post_category = ex
                        action.move_to_element(author).perform()
                        time.sleep(2)
                        try:
                            post_and_comment_karma = driver.find_elements(By.CLASS_NAME, '_18aX_pAQub_mu1suz4-i8j')
                            post_karma = post_and_comment_karma[0]
                            comment_karma = post_and_comment_karma[1]
                        except Exception as ex:
                            post_karma = ex
                            comment_karma = ex
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
                        print(f"{i+1} link done, Cycle time spent: {cycle_end_time} sec")

            except (WebDriverException, MaxRetryError) as ex:
                if time.time() - start_time > MAX_WAIT:
                    raise ex
                time.sleep(0.5)
            finally:
                print(f"Recording time spent: {(time.time() - start_time)//60} min")
                driver.close()
                driver.quit()


def main():
    get_data()
    get_data_urls()
    get_data_to_record()


if __name__ == '__main__':
    programm_start = time.time()
    main()
    print(f"Total time spent{(time.time() - programm_start) // 60} min")
