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
    @discord.ui.button(label="릴리즈 노트 작성", style=discord.ButtonStyle.green)
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
                release_output = subprocess.check_output("gh release view --repo=GSM-MSG/SMS-Android --json body", shell=True).decode()
                await message.channel.send(content = f"변경사항들은 아래와 같고 pr이 업로드 됐을거야 확인해줘!\n```{release_output[9:-3]}```")
                os.system(f'gh pr create --repo=GSM-MSG/SMS-Android --title "🔀 :: (TAG: {release_tag}) - VersionCode: {pr_versioncode}, VersionName: {pr_versionname}" --body "## 🚀 Release Info \n - VersionCode: {pr_versioncode} \n- VersionName: {pr_versionname} " --base "master" --head "develop"')
                break
            
    # @discord.ui.button(label="백엔드 ERROR 로그보기", style=discord.ButtonStyle.red)
    # async def backend_error_log(self, interaction : discord.Interaction, button: discord.ui.Button):
    #     log_data = subprocess.check_output('aws logs filter-log-events --log-group-name sms-logs --log-stream-names i-02468f866c3293595 --filter-pattern ERROR'.split(" "))
    #     dict_log = json.loads(log_data)
    #     print(dict_log)
    #     test = []
    #     error_log = ''

        
    #     for i in dict_log["events"]:
    #         test.append(i["message"].split(" : ")[1])

    #     print(test)
        
    #     for i in test[:5]:
    #             error_log = error_log + i + '\n'

    #     await interaction.response.send_message(content = error_log)



bot.run(token)