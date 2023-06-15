import time
from dotenv import load_dotenv
import os
import requests

import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from discordwebhook import Discord

login_url = 'https://aws.fitcloud.co.kr/login?referTo=/dashboard'

load_dotenv()

login_data = {
    'Id': os.environ.get('username'),
    'password': os.environ.get('pwd')
}

chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument('headless')
chrome_option.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
chrome_option.add_argument('--disable-gpu')
chrome_option.add_argument('--lang=ko_KR')
chrome_option.add_argument("--window-size=1920,1080")
chrome_option.add_argument("start-maximized")
browser = webdriver.Chrome(options=chrome_option)
browser.get(login_url)

time.sleep(3)
elem_id = browser.find_element(By.ID, 'loginUserId')
elem_id.send_keys(login_data['Id'])
time.sleep(1)

elem_pw = browser.find_element(By.ID, 'loginPassword')
elem_pw.send_keys(login_data['password'])
time.sleep(1)

browser.find_element(By.ID, 'kt_login_signin_submit').click()
time.sleep(3)

wait = WebDriverWait(browser, 20)
wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'kt-widget16__items'), '$'))
soup = BeautifulSoup(browser.page_source, 'html.parser')

cost_dashboard_dict = {}
for aws, price in zip(soup.find_all('span', 'kt-widget16__date'), soup.find_all('span', 'kt-widget16__price')):
    cost_dashboard_dict.update({re.sub('\s', '', aws.get_text()): re.sub('\s', '', price.get_text())})

browser.quit()

discord_url = os.environ.get('discord_webhook_url')
discord_webhook = Discord(url=discord_url)
source_cost_data = list(cost_dashboard_dict.items())
total_cost = sum([float(i[1][1:]) for i in source_cost_data])

content = f'환율 : ' \
          f'현재 aws 총 비용: ${round(total_cost, 2)}\n' \
          f'각 서비스 별 비용:'
for service, cost in source_cost_data:
    content += f'\n\t{service}: {cost}'

discord_webhook.post(content=content)
