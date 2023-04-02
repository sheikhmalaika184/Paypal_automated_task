import os
import time
import re
import csv
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = '/Users/malaikasheikh/python/chromedriver'
admin_email = "example@gmail.com"
password = "1122"

# starting a browser 
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
options = Options()
options.add_argument("--window-size=1920,1200")
options.add_argument('--disable-blink-features=AutomationControlled')
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
TIMEOUT = 60

emails_file = open("emails.txt","r", encoding='UTF-8')
emails_list = emails_file.readlines()
emails_file.close()

def make_request(url):
  try:
    driver.get(url)
    time.sleep(5)
    email_element = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginSection"]/form/div[3]/div[1]/div[2]/div[1]/input')))
    email_element.send_keys(admin_email)
    next_button = driver.find_element(By.XPATH, '//*[@id="loginSection"]/form/div[3]/div[2]/button')
    next_button.click()
    time.sleep(5)
    pass_element = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginSection"]/form/div[4]/div[1]/div/div[1]/div[1]/input')))
    pass_element.send_keys(password)
    login_button = driver.find_element(By.XPATH, '//*[@id="loginSection"]/form/div[4]/div[3]/button')
    login_button.click()
    time.sleep(60)
    driver.get("https://www.paypal.com/myaccount/transfer/homepage/request")
    time.sleep(5)
    e_count = 0
    while(e_count < 16):
      try:
        email = emails_list[0]
        emails_list.pop(0)
        email = email.replace("\n","")
        emails_input = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipientAutoCompleteWrapper"]/div/input')))
        emails_input.send_keys(email)
        time.sleep(1)
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recipientAutoCompleteWrapper"]/div/input'))).send_keys(Keys.ENTER)
        e_count = e_count + 1
      except Exception as ex:
        print(ex)
        break
  except Exception as e:
    print(e)
    pass
  
  emails_file = open("emails.txt","w", encoding='UTF-8')
  emails_file.writelines(emails_list)
  emails_file.close()
make_request('https://www.paypal.com/us/signin')
