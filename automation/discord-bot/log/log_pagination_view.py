import discord

class MainView(discord.ui.View):
    @discord.ui.button(label="백엔드 로그 보여주라..", style=discord.ButtonStyle.grey)
    async def fetch_backend_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="아 뭔 로그 볼껀데;;")