import discord

from load_cloudwatch_log import load_log


class LogPaginationView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.ctx = ctx

    @discord.ui.button(label="INFO", style=discord.ButtonStyle.grey, emoji="✅")
    async def show_info_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        # log = load_log("INFO", log_amount)
        await self.ctx.send("testset")

    @discord.ui.button(label="WARN", style=discord.ButtonStyle.grey, emoji="⚠️")
    async def show_warn_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.ctx.send("testset")

    @discord.ui.button(label="ERROR", style=discord.ButtonStyle.grey, emoji="‼️")
    async def show_info_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.ctx.send("testset")

    @discord.ui.button(label="다 보여줘!", style=discord.ButtonStyle.grey, emoji="️😄")
    async def show_info_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.ctx.send("testset")