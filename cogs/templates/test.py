import discord
from discord import app_commands, Interaction as inter
from discord.ext import commands

# Define the class for your cog
class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Optional: Add any setup code here
    @commands.Cog.listener()
    async def on_ready(self):
        print('MyCog is ready.')

    @app_commands.command(name="echo", description="echo your words into the abyss...")
    async def echo(self, intr: inter):
        await intr.response.send_message("Hi")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(MyCog(bot))
