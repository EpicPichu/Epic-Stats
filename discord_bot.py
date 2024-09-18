import discord
from discord.ext import commands
from discord import Interaction as inter, app_commands
import os
from dotenv import load_dotenv
load_dotenv()

EpicPichu = 598085365815050241


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')



    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')
            print(f'Loaded extension: {file[:-3]}')
            
    await bot.tree.sync()



@bot.tree.command(name='ping', description='The latency between client host and server host')
async def ping(intr:inter):
    latency = round(bot.latency*1000)
    await intr.response.send_message(content=f'Ping: {latency} ms.')

@bot.tree.command(name='extensions', description='List all the loaded extensions')
async def extensions(intr:inter):
    if intr.user.id == EpicPichu:
        loaded_extensions = [extension.replace('cogs.', '') for extension in bot.extensions]
        extensions_list = "\n".join(loaded_extensions)
        await intr.response.send_message("Loaded extensions:\n\n" + extensions_list)
    else:
        await intr.response.send_message("You are not allowed to do this!")


@bot.tree.command(name='unload', description='Unload any specific extension')
@app_commands.describe(ext='Specify the extension to unload')

async def unload(intr:inter, ext:str):
    if intr.user.id == EpicPichu:

        await bot.unload_extension(f'cogs.{ext}')
        await intr.response.send_message(f'Unloaded {ext}.')
    else:
        await intr.response.send_message("You are not allowed to do this!")



@bot.tree.command(name='reload', description='Reloads all the extensions of this bot')
async def reload(intr:inter):

    if intr.user.id == EpicPichu:
        # Get a list of all Python files in the 'cogs' directory
        cog_files = [filename[:-3] for filename in os.listdir('./cogs') if filename.endswith('.py')]
        
        # Get a list of currently loaded extensions
        loaded_extensions = [extension.replace('cogs.', '') for extension in bot.extensions]

        # Check for new extensions to load
        for cog in cog_files:
            if cog not in loaded_extensions:
                await bot.load_extension(f'cogs.{cog}')
                await intr.channel.send(f'Loaded new extension: {cog}')
        
        # Reload all loaded extensions
        extension_list = dict(bot.extensions)

        for extension in extension_list:
            await bot.reload_extension(extension)
        await intr.response.send_message("All extensions reloaded.")

        await bot.tree.sync()
    else:
        await intr.response.send_message("You are not allowed to do this!")

    

bot.run(os.getenv('token'))

# ily_pichu >//< crazy