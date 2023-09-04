import os

import dotenv

import discord
from discord.ext import commands

from log_pagination_view import MainView

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

bot = commands.Bot(command_prefix=("ㅅ ", "성훈아 "), intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("이번 인수합병은 만족스러웠습니다")

@bot.command()
async def 안녕(ctx):
    await ctx.send('난 부자다 으하하하')


@bot.command(aliases=['ㄹ'])
async def 도와줘(ctx, log_type, log_amount):
    view = MainView()
    # log = load_log(log_type, log_amount)
    await ctx.reply("아~ 귀찮게 또 뭘 시키는거야", view)

bot.run(os.environ["TOKEN"])