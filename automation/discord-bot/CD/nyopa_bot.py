from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
import requests
import os
import json
import subprocess
from pprint import pprint

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

load_dotenv()
token = os.getenv("token")
channel_url = os.getenv("channel")
ios_channel_url = os.getenv("ios_channel")
ios_gittoken = os.getenv("ios_gittoken")

@bot.event
async def on_ready():
    print("I'm ready")

@bot.command()
async def 뇨파(ctx):
    view = Deploy()
    await ctx.reply("뇨~ 뭘 도와줄까?",view=view)

class Deploy(discord.ui.View):
    @discord.ui.button(label="안드로이드 릴리즈 노트 작성", style=discord.ButtonStyle.green)
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
                    try:
                        subprocess.check_output(f'gh release create {release_tag} --repo=GSM-MSG/SMS-Android --title={release_title} --generate-notes'.split(" "))
                    except subprocess.CalledProcessError as e:
                        print(e.returncode)
                        print(e.output)
                    await message.channel.send(content = "뇨 ~ 릴리즈 노트를 작성했어. 바로 pr 올리기를 통해서 배포 준비를 진행해줘!")
                break
    
    @discord.ui.button(label="안드로이드 Merge PR 올리기", style=discord.ButtonStyle.green)
    async def android_pull_request(self, interaction : discord.Interaction, button: discord.ui.Button):
        global release_tag
        global release_title
        
        member = interaction.user
        channel = bot.get_channel(int(channel_url))
        await interaction.response.send_message(content = "develop에서 master로 머지하는 pr를 올릴게. 버전 코드와 버전 이름을 알려줘. \n 예시)5,1.0.0")
        while(True):
            try: 
                message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=30.0)
            except asyncio.TimeoutError:
                await message.channel.send("30초가 지났어. 명령어를 다시 실행시켜줘.")
            else:
                pr_versioncode = message.content[0]
                pr_versionname = message.content[2:]
                release_tag = (str(subprocess.check_output("gh release list --repo=GSM-MSG/SMS-Android --limit 1", shell=True, encoding='utf-8')).split("\t"))[2]
                release_output = subprocess.check_output("gh pr list --repo=GSM-MSG/SMS-Android --json url --limit 1", shell=True, encoding='utf-8').decode()
                await message.channel.send(content = f"변경사항들은 아래와 같고 pr이 업로드 됐을거야 확인해줘!\n{release_output}")
                os.system(f'gh pr create --repo=GSM-MSG/SMS-Android --title "🔀 :: (TAG: {release_tag}) - VersionCode: {pr_versioncode}, VersionName: {pr_versionname}" --body "## 🚀 Release Info \n - VersionCode: {pr_versioncode} \n- VersionName: {pr_versionname} " --base "master" --head "develop"')
                break
            
    @discord.ui.button(label="iOS 워크플로우 실행", style=discord.ButtonStyle.green)
    async def ios_deploy(self, interaction : discord.Interaction, button: discord.ui.Button):
        global release_tag
        global release_title
        
        member = interaction.user
        channel = bot.get_channel(int(ios_channel_url))
        await interaction.response.send_message(content = "릴리즈 버전을 작성해줘.")
        while(True):
            try: 
                message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=30.0)
            except asyncio.TimeoutError:
                await message.channel.send("30초가 지났어. 명령어를 다시 실행시켜줘.")
            else:
                release_version  = message.content
                await message.channel.send(content = "변경사항을 작성해줘.")
                try: 
                    message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=30.0)
                except asyncio.TimeoutError:
                    await message.channel.send("30초가 지났어. 명령어를 다시 실행시켜줘.")
                else:
                    release_content = message.content
                    try:
                        headers = {'Authorization': f'token {ios_gittoken}', 'Accept': 'application/vnd.github+json'}
                        requests.post('https://api.github.com/repos/GSM-MSG/SMS-iOS/actions/workflows/67054831/dispatches', 
                                        json = {"ref": "master",
                                                "inputs": {
                                                    "version": f"{release_version}",
                                                    "changed": f"{release_content}"}
                                        },
                                        headers=headers
                                        )
                    except subprocess.CalledProcessError as e:
                        print(e.returncode)
                        print(e.output)
                    await message.channel.send(content = "뇨 ~ 다른 친구에서 requets를 보냈어! 그 친구가 제대로 일하고 있는지 확인해줘!")
                break

bot.run(token)
