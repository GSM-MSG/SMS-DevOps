from dotenv import load_dotenv
import os
import argparse
import asyncio
import aiohttp
from discord import Webhook, Embed, Color

parser = argparse.ArgumentParser(description='Add two numbers.')

# positional arguments 정의
parser.add_argument('category', type=str, help='system category e.g) cpu, mem, disk')
parser.add_argument('usage', type=int, help='usage of first arugment e.g) 100, 60, 55')
args = parser.parse_args()

load_dotenv()
discord_url = os.getenv('DISCORD_URL')
Content = Embed(
    title='리소스 사용량 경고',
    description='서버의 리소스 사용량이 높습니다.',
    color=Color.random())

Content.add_field(name=f'{args.category}', value=f'{args.usage}%', inline=False)

Content.set_footer(text='으악 서버 죽어욧')

async def send_fee_data(content):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(discord_url, session=session)
        await webhook.send(embed=content, username='서버 리소스 와처')


asyncio.run(send_fee_data(Content))
