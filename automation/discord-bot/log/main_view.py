import discord

from log_view import LogPaginationView

class MainView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.ctx = ctx

    @discord.ui.button(label="백엔드 로그 보여주라..", style=discord.ButtonStyle.grey)
    async def fetch_backend_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = LogPaginationView(self.ctx)
        await self.ctx.reply("또? 무슨 로그 볼껀데;", view=view)