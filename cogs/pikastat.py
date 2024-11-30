import discord, aiohttp, sqlite3, json
from discord import app_commands, Interaction as inter
from discord.ext import commands
from typing import Literal
from datetime import datetime, timezone

# Define the class for your cog
class pikastat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = 0xFF5555
        self.icon_url = 'https://images-ext-1.discordapp.net/external/BMxv53EwbvT_wkNbNFvf7IG3lD1NWMLDC96Ny7s9pqU/https/i.imgur.com/D3uyBf8.png'
        self.connection = sqlite3.connect('names.db')
        self.db = self.connection.cursor()

        new_table = '''
        CREATE TABLE IF NOT EXIST users(
        lowername TEXT NOT NULL,
        realname TEXT NOT NULL
        );
        '''
        self.db.execute(new_table)
        self.connection.commit()
        self.api_dict = {
            "OpFactions": "opfactions",
            "OpPrison": "opprison",
            "OpSkyBlock": "opskyblock",
            "Skyblock": "classicskyblock",
            "Survival": "survival",
            "KitPvP": "kitpvp",
            "Unranked Practice": "unrankedpractice",
            "Ranked Practice": "rankedpractice",
            "Bedwars": "bedwars",
            "Skywars": "skywars",
            "LifeSteal": "lifesteal",
            "OpLifeSteal": "oplifesteal",
            "SkyPvP": "skypvp"
        }

        self.interval_dict = {
            "Weekly": "weekly",
            "Monthly": "monthly",
            "Yearly": "yearly"
        }










    @app_commands.describe(
        username = 'Username that you would like to check.',
        gamemode = 'Gamemode that you would like to check.',
        interval = 'Interval that you would like to check.'
    )

    @app_commands.command(name="stats", description="Check stats for username per gamemode.")
    async def stats(self, intr: inter,
        
        username: str,
        gamemode: Literal[
        "OpFactions",
        "OpPrison",
        "OpSkyBlock",
        "Skyblock",
        "Survival",
        "KitPvP",
        "Unranked Practice",
        "Ranked Practice",
        "Bedwars",
        "Skywars",
        "LifeSteal",
        "OpLifeSteal",
        "SkyPvP"
        ],

        interval: Literal['Weekly', 'Monthly', 'Yearly'] = 'total'

        ):

        async with aiohttp.ClientSession() as session:

            query = self.db.execute('SELECT * FROM users WHERE lowername = ?', (username.lower(),))
            output = query.fetchall()

            if output:
                realname = output[0][1]

            else:
                async with session.get(f'https://stats.pika-network.net/api/profile/{username}') as response:

                    if response.status != 200:
                        pass
                    
                    api = await response.json()
                    realname = api['username']
                    
                    self.db.execute("INSERT INTO users (lowername, realname) VALUES (?, ?)", (username.lower(), realname))
                    self.connection.commit()

            async with session.get(f'https://stats.pika-network.net/api/profile/{realname}/leaderboard?type={self.api_dict[gamemode]}&interval={interval}&mode=ALL_MODES') as response:
                data = await response.text()
                api = json.loads(data)
                lines = ''''''

                for key, entry in api.items():
                    if entry['entries']:
                        place = entry['entries'][0]['place']
                        value = entry['entries'][0]['value']
                        lines = lines + (f'- #{place} | {key}: **{value}**\n')
                    else:
                        pass
                if not lines: lines = '''- _Looks like there are no entries for this query :thinking:_'''

                def fet(entry):
                    js = api[entry]['entries']
                    return (js[0]['value'], js[0]['place']) if js else ('0', '0')



        embed = discord.Embed(
            color=self.embed_color,
            timestamp= datetime.now(timezone.utc),
            description=f'''Below are total **{gamemode}** stats for `{realname}`:\n\n{lines}'''
            )
        embed.set_footer(text="PikaNetwork Stats", icon_url=self.icon_url)

        await intr.response.send_message(embed=embed)

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(pikastat(bot))
