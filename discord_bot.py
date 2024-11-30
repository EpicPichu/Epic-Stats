import discord, requests, shutil
from discord.ext import commands
from discord import Interaction as inter, app_commands
import os
from dotenv import load_dotenv
load_dotenv()
from typing import Literal

EpicPichu = 598085365815050241
repo_owner = 'EpicPichu'
repo_name = 'Epic-Stats'
branch = 'main'

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














def clear_directory(local_path):
    """Clear all files and folders in the target directory."""
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    os.makedirs(local_path, exist_ok=True)

def syncc(repo_owner, repo_name, branch, folder_path, local_path):
    clear_directory(local_path)

    # GitHub API URL for folder contents
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}?ref={branch}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)

    outp = ""

    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item["type"] == "file":
                file_url = item["download_url"]
                file_name = item["name"]

                try:
                    file_response = requests.get(file_url)
                    file_response.raise_for_status()  # Raise an error for bad responses
                    os.makedirs(local_path, exist_ok=True)  # Ensure directory exists
                    with open(os.path.join(local_path, file_name), "wb") as f:
                        f.write(file_response.content)

                    outp += f"Downloaded {file_name}\n"
                except requests.RequestException as e:
                    outp += f"Failed to download {file_name}: {e}\n"

            elif item["type"] == "dir":
                # Recursively download subdirectories
                subfolder_path = item["path"]
                subfolder_local_dir = os.path.join(local_path, item["name"])
                outp += syncc(repo_owner, repo_name, branch, subfolder_path, subfolder_local_dir)
    else:
        outp += f"Failed to fetch contents: {response.status_code}, {response.text}\n"

    return outp
















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



@bot.tree.command(name='sync', description='Reloads the bot with freshly pulled code from github')
async def reload(intr:inter,
    folder: Literal['cogs', 'assets'] = 'cogs'
    ):

    if intr.user.id == EpicPichu:

        await intr.response.send_message('Downloading...', ephemeral=True)

        response = syncc(repo_owner, repo_name, branch, folder, f'./{folder}')

        # Get a list of all Python files in the 'cogs' directory
        cog_files = [filename[:-3] for filename in os.listdir('./cogs') if filename.endswith('.py')]
        
        # Get a list of currently loaded extensions
        loaded_extensions = [extension.replace('cogs.', '') for extension in bot.extensions]

        new_extensions = ""

        # Check for new extensions to load
        for cog in cog_files:
            if cog not in loaded_extensions:
                await bot.load_extension(f'cogs.{cog}')
                new_extensions += f"Loaded extension: {cog}\n"
        
        # Reload all loaded extensions
        extension_list = dict(bot.extensions)

        for extension in extension_list:
            await bot.reload_extension(extension)

        await intr.edit_original_response(content=(response + '\n\n\n' + new_extensions))

        await bot.tree.sync()
    else:
        await intr.response.send_message("You are not allowed to do this!", ephemeral=True)

bot.run(os.getenv('token'))



# ily_pichu >//< crazy