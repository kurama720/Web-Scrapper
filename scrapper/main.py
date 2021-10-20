import uuid

import requests
from bs4 import BeautifulSoup


url = 'https://www.reddit.com/top/?t=month'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
links = soup.find_all('a', class_='SQnoC3ObvgnGjWt90zD9Z')
records = soup.find_all('div', class_='_2SdHzo12ISmrC8H86TgSCp')
authors = soup.find_all('a', class_='_2tbHP6ZydRpjI44J3syuqC')


with open('reddit-YYYYMMDDHHMM.txt', 'w') as f:
    for i in range(0, len(records)):
        f.write(f"UNIQUE_ID: {uuid.uuid4()}; URL: https://www.reddit.com/{links[i].get('href')}; TEXT:{records[i].text}\n")
