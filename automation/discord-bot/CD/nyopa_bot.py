from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
import os
import json
import subprocess
from pprint import pprint

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

load_dotenv()
token = os.getenv("token")
channel_url = os.getenv("channel")

@bot.event
async def on_ready():
    print("I'm ready")

@bot.command()
async def 뇨파(ctx):
    view = Deploy()
    await ctx.reply("뇨~ 뭘 도와줄까?",view=view)

class Deploy(discord.ui.View):
    @discord.ui.button(label="안드로이드 배포", style=discord.ButtonStyle.green)
    async def android_deploy(self, interaction : discord.Interaction, button: discord.ui.Button):
        global release_tag
        global release_title
        
        member = interaction.user
        channel = bot.get_channel(int(channel_url))
        await interaction.response.send_message(content = "릴리즈 타이틀을 작성해줘.")
        while(True):
            try: 
                message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=30.0)
            except asyncio.TimeoutError:
                await message.channel.send("30초가 지났어. 명령어를 다시 실행시켜줘.")
            else:
                release_title  = message.content
                await message.channel.send(content = "릴리즈 태그를 작성해줘.")
                try: 
                    message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=30.0)
                except asyncio.TimeoutError:
                    await message.channel.send("30초가 지났어. 명령어를 다시 실행시켜줘.")
                else:
                    release_tag = message.content
                    await message.channel.send(content = "뇨 ~ Default 브랜치로 CD를 진행할게. 무사히 올라가길 같이 기도해줘.")
                    os.system(f'gh release create {release_tag} --repo=GSM-MSG/SMS-Android --title={release_title} --generate-notes')
                break

    @discord.ui.button(label="백엔드 ERROR 로그보기", style=discord.ButtonStyle.red)
    async def backend_log(self, interaction : discord.Interaction, button: discord.ui.Button):
        log_data = subprocess.check_output('aws logs filter-log-events --log-group-name sms-logs --log-stream-names i-02468f866c3293595 --filter-pattern ERROR'.split(" "))
        dict_log = json.loads(log_data)
        
        test = []
        error_log = ''

        for i in dict_log["events"]:
            test.append(i["message"].split(" : ")[1])

        for i in test[:20]:
                error_log = error_log + i + '\n'

        await interaction.response.send_message(content = error_log)



bot.run(token)