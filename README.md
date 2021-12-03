# Scrapper for reddit.com

---
## What does it use?
- **Python 3.8**
- **PostgreSQL**, **Psycopg2**
- **Selenium**
- **BeautifulSoup**
- **MongoDB**, **PyMongo**
- **Git**

## How to install?

---

1. ```$ git clone https://github.com/kurama720/iTechArtLab.git```
2. Download _chromedriver.exe_ here _https://chromedriver.chromium.org/downloads_. Choose version according to your
**Chrome** version.
3. Put driver in _iTechArt/scrapper_ directory.
4. If Windows user, copy an absolute path to driver and write in selenium_driver.py.
5. Install requirements.

## How it works?

---
It parses **reddit.com** with _BeautifulSoup_ and _Selenium_. Searches for given amount of posts in category _Top ->
This Month_. Pulls such info as: _post URL_, _author's username_, _author's karma_, _cake day_, _post karma_,
_comment karma_, _post date_, _number of comments_, _number of votes_ and _post category_. Assigns a unique id with
uuid4() and sends it to the server.
Divides data on author data and post data. Saves it in database, into two tables/collections _author_ and _post_.
Scrapping takes ~15 minutes.  
Creates API processing request methods as GET, POST, PUT, DELETE. Takes data from database.
Field *_id* is to be given with post request.

## How to run?
---
To run server and select database execute this in the folder iTechArt/:  
```$ python execute.py -a runserver```  

To run scrapper execute this, where -r takes an amount of records to be pulled:  
```$ python execute.py -r <amount> -a runscrapper```   

To show logs:  
```$ python execute.py -a logs```

To run API on postgreSQL make following steps:

1. Type your _username_, _password_ to PostgreSQL and existing _database_ in directory _database/constant_data.py_.
2. Create database and tables with running this in the foled iTechArt/:  
```% python execute.py -a createvault```


## How was it tested?

---
The **Postman** application was used to test request methods to API.  
Database and scrapper were tested only manually.