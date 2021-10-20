from bs4 import BeautifulSoup
import requests

url = 'https://www.reddit.com/top/?t=month'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
authors = soup.find_all('a', class_='_2tbHP6ZydRpjI44J3syuqC')
first_div = soup.find('div', class_='_14-YvdFiW5iVvfe5wdgmET')
second_div = first_div.find('div', class_='cZPZhMe-UCZ8htPodMyJ5')
third_div = second_div.find('div', class_='_2mHuuvyV9doV3zwbZPtIPG')
first_a = third_div.find('a')
print(first_a.text)


#
# dict1 = {}
#
# while True:
#     for i in range(0, len(records)):
#         dict1['URL'] = 'https://www.reddit.com/' + links[i].get('href')
#         dict1['TEXT'] = records[i].text
#         for j in range(0, len(authors)):
#             author_profile = authors[j].get('href')
#             author_response = requests.get(author_profile)
#             author_soup = BeautifulSoup(author_response.text, 'lxml')
#             username = author_soup.find_all('span', class_='_1LCAhi_8JjayVo7pJ0KIh0')
#             dict1['AUTHOR'] = username.text
#
#     print(dict1)
#

# for j in range(0, len(authors)):
#     author_profile = authors.get('href')
#     author_response = requests.get(author_profile)
#     author_soup = BeautifulSoup(author_response.text, 'lxml')
#     username = author_soup.find('span', class_='_1LCAhi_8JjayVo7pJ0KIh0')
#     print(username)