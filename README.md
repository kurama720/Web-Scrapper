# Scrapper for reddit.com

---
## How it works?

---
**It parses reddit.com with BeautifulSoup and Selenium. Searches for 100 posts in category Top -> This Month. Pulls such
info as: post URL, author's username, author's karma, cake day, post karma, comment karma, post date, number of 
comments, number of votes and post category. Also assigns a unique id for each record with uuid. Writes this info into a
txt file named reddit-YYYY-MM-DD-HH-MM, where YYYY - year, MM - month, DD - day, HH - hour, MM - minute. Scrapping takes
~15 minutes.**

## How to run?

___
**Execute function** _main.py_ **in module _main.py_ in the directory _scrapper_**
