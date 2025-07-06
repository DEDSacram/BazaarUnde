import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
import json


import undetected_chromedriver as uc




driver = uc.Chrome(headless=False)

#login
driver.get('https://www.facebook.com/marketplace')

#wait for you to sign up get cookies
time.sleep(120)



# Pull current cookies
cookies = driver.get_cookies()

# Print them
for cookie in cookies:
    print(cookie)

with open("cookies2.json", "w") as f:
    json.dump(cookies, f)

