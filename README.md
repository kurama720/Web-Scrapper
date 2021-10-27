# Scrapper for reddit.com

---
## How it works?

---
**It parses reddit.com with** _BeautifulSoup_ **and** _Selenium_**. Searches for 100 posts in category** _Top -> This 
Month_**.** **Pulls such info as:** _post URL_**,** _author's username_**,** _author's karma_**,** _cake day_**,**
_post karma_**,** _comment karma_**,** _post date_**,** _number of comments_**,** _number of votes_ **and** _post
category_**. Also assigns a** _unique id_ **for each record with** _uuid_. **Writes this info into a txt file named** 
_reddit-YYYY-MM-DD-HH-MM_, **where** _YYYY_ **- year,** _MM_ **- month,** _DD_ **- day,** _HH_ **- hour,** _MM_ **- 
minute. Scrapping takes ~15 minutes.**

## How to run?

___
**Execute function** _main.py_ **in module** _main.py_ **in the directory** _scrapper_
