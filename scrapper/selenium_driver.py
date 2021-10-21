from selenium import webdriver


chromedriver = 'D:\\iTechArt\\scrapper\\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')

driver = webdriver.Chrome(options=options)
driver.maximize_window()
