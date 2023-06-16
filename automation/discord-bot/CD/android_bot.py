from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
import sys
import os

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

load_dotenv()
token = os.getenv("token")
channel_url = os.getenv("channel")

@bot.event
async def on_ready():
    print("I'm ready")

@bot.command()
async def 배포(ctx):
    view = Deploy()
    await ctx.reply("뇨~ 어떤 배포를 도와줄까?",view=view)

class Deploy(discord.ui.View):
    
    @discord.ui.button(label="안드로이드 배포", style=discord.ButtonStyle.green)
    async def android_deploy(self, interaction : discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        channel = bot.get_channel(int(channel_url))
        await interaction.response.send_message(content = "릴리즈 타이틀을 입력해주세요.")

        while(True):
            try: 
                message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=30.0)
            except asyncio.TimeoutError:
                await message.channel.send("30초가 지났어요. 명령어를 다시 실행시켜주세요.")
            else:
                await message.channel.send(content = "릴리즈 노트를 입력해주세요.")
                try: 
                    message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=30.0)
                except asyncio.TimeoutError:
                    await message.channel.send("30초가 지났어요. 명령어를 다시 실행시켜주세요.")
                else:
                    await message.channel.send(content = "Default 브랜치로 CD를 진행할게요. 무사히 올라가길 같이 기도해주세요.")
                break


bot.run(token)