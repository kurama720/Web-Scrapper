from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
options.add_argument('headless')

driver = webdriver.Chrome(options=options)
driver.maximize_window()
