import os

import dotenv

import discord
from discord.ext import commands

from load_cloudwatch_log import load_log


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

bot = commands.Bot(command_prefix=("ㅅ ", "성훈아 "), intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("이번 인수합병은 만족스러웠습니다")

@bot.command(aliases=['ㄹ'])
async def 로그보여줘(ctx, log_type, log_amount):
    log = load_log(log_type, log_amount)
    await ctx.send('\n'.join(log[0]))

@bot.command()
async def 안녕(ctx):
    await ctx.send('난 부자다 으하하하')


bot.run(os.environ["TOKEN"])