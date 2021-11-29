"""Creates a driver for selenium to parse and imitate mouse hover"""

from selenium import webdriver

# Configure necessary options
options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# Create a driver and add him the options
# If Windows user write an absolute path to driver here in field <executable_path>
driver = webdriver.Chrome(options=options, executable_path=r'D:\iTechArt\scrapper\chromedriver.exe')
driver.maximize_window()
driver.implicitly_wait(20)
