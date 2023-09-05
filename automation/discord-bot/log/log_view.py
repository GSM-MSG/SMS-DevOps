import asyncio

import discord

from load_cloudwatch_log import load_log


class LogLevelSelectionView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=20)
        self.ctx = ctx

    async def on_timeout(self) -> None:
        await self.ctx.send("늦었어. 난 충분히 기다렸다.")

    @discord.ui.button(label="INFO", style=discord.ButtonStyle.grey, emoji="✅")
    async def show_info_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        log_data = load_log('INFO', 1000)
        log_page = LogPaginationView(self.ctx, log_data)
        await log_page.send()

    @discord.ui.button(label="WARN", style=discord.ButtonStyle.grey, emoji="⚠️")
    async def show_warn_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        log_data = load_log('WARN', 1000)
        log_page = LogPaginationView(self.ctx, log_data)
        await log_page.send()

    @discord.ui.button(label="ERROR", style=discord.ButtonStyle.grey, emoji="‼️")
    async def show_error_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        log_data = load_log('ERROR', 1000)
        log_page = LogPaginationView(self.ctx, log_data)
        await log_page.send()

    @discord.ui.button(label="다 보여줘!", style=discord.ButtonStyle.grey)
    async def show_all_log(self, interaction: discord.Interaction, button: discord.ui.Button):
        log_data = load_log('ALL', 1000)
        log_page = LogPaginationView(self.ctx, log_data)
        await log_page.send()


class LogPaginationView(discord.ui.View):
    def __init__(self, ctx, data):
        super().__init__(timeout=10)
        self.ctx= ctx
        self.data = data[0]
        self.data.reverse()
        self.metadata = data[1]

        self.current_page : int = 1
        self.sep : int = 10

    async def on_timeout(self) -> None:
        await self.ctx.send("갔냐?")

    async def send(self):
        self.message = await self.ctx.send(view=self)

    def create_embed(self, data):
        embed = discord.Embed(title="Backend Log")
        for item in data:
            embed.add_field(name=item, value=item, inline=False)
        return embed

    async def update_message(self, data):
        await self.message.edit(embed=self.create_embed(data), view=self)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:until_item])

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:until_item])

