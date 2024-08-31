import discord
from discord import app_commands, Interaction as inter
from discord.ext import commands 
from  typing import Literal
import aiohttp
from io import BytesIO



# Define the class for your cog
class sus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Optional: Add any setup code here
    @commands.Cog.listener()
    async def on_ready(self):
        print('MyCog is ready.')


    
    @app_commands.describe(
            
        username='Type the username of the player',
        interval='Specify the interval',
        gamemode='Specify the gamemode'        
        
        )

    @app_commands.command(name="sus", description="test af")
    async def sus(
        self, interaction: inter,

        username: str ,
        interval: Literal['Lifetime', 'Yearly', 'Monthly', 'Weekly'] = 'Lifetime' ,
        gamemode: Literal['All_Modes', 'Solo', 'Doubles', 'Triples', 'Quads'] = 'All_Modes'

    ):
        
        initial_message = await interaction.response.send_message("Downloading image, please wait...")

        async with aiohttp.ClientSession() as session:
            url = f"http://127.0.0.1/bedwars/{username}?interval={interval}&mode={gamemode}"
            async with session.get(url) as response:
                image_bytes = await response.read()
                image_data = BytesIO(image_bytes)
                image_data.seek(0)

        discord_file = discord.File(fp=image_data, filename="image.png")

        await interaction.edit_original_response(content=(f'{username}\n{interval}\n{gamemode}'), attachments=[discord_file])










# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(sus(bot))
