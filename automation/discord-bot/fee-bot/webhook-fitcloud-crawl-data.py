import asyncio
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

from discord import Webhook, Embed, Color
import aiohttp

login_url = 'https://aws.fitcloud.co.kr/login?referTo=/dashboard'

load_dotenv()

login_data = {
    'Id': os.environ.get('username'),
    'password': os.environ.get('pwd')
}
user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument('headless')
chrome_option.add_argument(f'--user-agent={user_agent["User-Agent"]}')
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

wait = WebDriverWait(browser, 40)
wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'kt-widget16__items'), '$'))
soup = BeautifulSoup(browser.page_source, 'html.parser')


source_cost_data = list()
for aws, price in zip(soup.find_all('span', 'kt-widget16__date'), soup.find_all('span', 'kt-widget16__price')):
    source_cost_data.append((re.sub('\s', '', aws.get_text()), re.sub('\s', '', price.get_text())))

browser.quit()

discord_url = os.environ.get('discord_webhook_url')
total_cost = sum([float(i[1][1:]) for i in source_cost_data])

KRW_url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
exchange = requests.get(KRW_url, headers=user_agent).json()
exchange_rate = exchange[0]['basePrice']

Content = Embed(
    title='aws 요금',
    description=
        f'## 오늘의 환율은 1$ 당 {exchange_rate}₩ 입니다.\n'
        f'총 비용은 {total_cost:.2f}$ {total_cost*exchange_rate:.2f}₩ 이고\n'
        f'각 서비스 별 비용은 아래와 같습니다.',
    color=Color.random())

for service, cost in source_cost_data:
    Content.add_field(name=service, value=cost, inline=False)

period = soup.find_all('span', 'kt-widget24__desc')[1].get_text()
Content.set_footer(text=f'{period} 까지의 비용 입니다.')


async def send_fee_data(content):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(discord_url, session=session)
        await webhook.send(embed=content, username='aws 비용 봇')

asyncio.run(send_fee_data(Content))