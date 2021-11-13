import requests

url = 'http://127.0.0.1:8087/posts'
url_with_id = 'http://127.0.0.1:8087/posts/'  # put  UNIQUE ID after posts/


data = {'POST_URL': 'https://www.reddit.com/r/MadeMeSmile/comments/qkq3a2/my_kid_was_a_little_sad_after_not_seeing_any/'
        , 'AUTHOR': 'slava', 'USER KARMA': '187k', 'CAKE DAY': 'October 31 2015', 'COMMENTS NUMBER': '1.3k Comments'
        , 'VOTES NUMBER': '250k', 'POST CATEGORY': 'MadeMeSmile', 'POST KARMA': '32k', 'COMMENT KARMA': '0k',
        'POST DATE': '21-8-2021'}
data_to_update = {'AUTHOR': 'slava', 'VOTES NUMBER': 'no votes found'}

requests.delete(url=url_with_id)
requests.put(url=url_with_id, data=data_to_update)
requests.post(url=url, data=data)
