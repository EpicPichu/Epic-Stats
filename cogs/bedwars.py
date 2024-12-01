import discord, sqlite3, datetime, asyncio, aiohttp, time
from discord import app_commands, Interaction as inter
from discord.ext import commands 
from  typing import Literal
from main.images import *


# Define the class for your cog
class bedwars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.connection = sqlite3.connect('names.db')
        self.db = self.connection.cursor()

        create_table = '''
        CREATE TABLE IF NOT EXISTS users(
        lowername TEXT NOT NULL,
        realname TEXT NOT NULL
        );
        '''
        self.db.execute(create_table)
        self.connection.commit()
    
    @app_commands.describe(
            
        username='Type the username of the player',
        interval='Specify the interval',
        gamemode='Specify the gamemode'        
        
        )

    @app_commands.command(name="bedwars", description="Fecth bedwars stats of a player")
    async def bedwars(
        self, interaction: inter,

        username: str ,
        interval: Literal['Lifetime', 'Yearly', 'Monthly', 'Weekly'] = 'Lifetime' ,
        gamemode: Literal['All_Modes', 'Solo', 'Doubles', 'Triples', 'Quads'] = 'All_Modes'

    ):

        start = time.time()
        initial_message = await interaction.response.send_message("Downloading image, please wait...")


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

            profilereq = session.get(f'https://stats.pika-network.net/api/profile/{realname}')
            statsreq = session.get(f'https://stats.pika-network.net/api/profile/{realname}/leaderboard?type=BEDWARS&interval={interval}&mode={gamemode}')
            modelreq = session.get(f"https://starlightskins.lunareclipse.studio/render/custom/"+realname+"/full?wideModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/models/tnt_sit/pose1.obj&slimModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/models/tnt_sit/pose1.obj&propModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/models/tnt_sit/pose1prop.obj&propTexture=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/models/tnt_sit/tnt.png&cameraPosition={%22x%22:%228.47%22,%22y%22:%2223.06%22,%22z%22:%22-30.87%22}&cameraFocalPoint={%22x%22:%224%22,%22y%22:%2219%22,%22z%22:%22-16.24%22}&cameraFOV=45&cameraWidth=374&cameraHeight=437")

            profile, model, stats = await asyncio.gather(profilereq, modelreq, statsreq)

            if profile.status != 200:
                pass

            api = await profile.json()

            username = api['username']

            level = str(api['rank']['level'])

            lvl = int(level)
            if 0 < lvl < 5:
                level_color = 'gray'
            elif 5<=lvl<10 or 40<=lvl<45:
                level_color = 'lime'
            elif 10<=lvl<15 or 45<=lvl<50:
                level_color = 'aqua'
            elif 15<=lvl<20 or 50<=lvl<60:
                level_color = 'pink'
            elif 20<=lvl<25 or  60<=lvl<75:
                level_color = 'orange'
            elif 25<=lvl<30 or 75<=lvl<100:
                level_color = 'yellow'
            elif 30<=lvl<35 or lvl==100:
                level_color = 'red'
            elif 35 <= lvl < 40:
                level_color = 'white'
            
            level_bold = lvl >= 35

            rank_colors = {
                'Champion': (170, 0, 0),     # Red
                'Titan': (255, 170, 0),      # Orange
                'Elite': (85, 255, 255),     # Cyan
                'VIP': (85, 255, 85),        # Green
                }
            
            ranksjson = str(api['ranks'])
            ranklist = ['Champion', 'Titan', 'Elite', 'VIP']
            rank = next((ranks for ranks in ranklist if ranks in ranksjson), None)
            rank_color = rank_colors.get(rank, (170, 170, 170))
            
            friends = len(api['friends'])

            if api['clan']:
                guild = 'GUILD'
                gName = api['clan']['name']
                gTag = api['clan']['tag']
                gLevel = str(api['clan']['leveling']['level'])
                gMembers = str(len(api['clan']['members']))
                gOwner = api['clan']['owner']['username']
            else:
                guild = 'NO GUILD'
                gName = gTag = gLevel = gMembers = gOwner = None

            def seen(unix_time_ms):
                # Convert Unix time with milliseconds to a datetime object
                unix_time_seconds = unix_time_ms / 1000.0
                timestamp = datetime.datetime.fromtimestamp(unix_time_seconds)

                # Calculate the time difference
                current_time = datetime.datetime.now()
                time_difference = current_time - timestamp

                # Convert the time difference into days, hours, and minutes
                days = time_difference.days
                hours = time_difference.seconds // 3600
                minutes = (time_difference.seconds % 3600) // 60

                # Format the time difference
                if days > 0:
                    return f"Seen: {days} days ago"
                elif hours > 0:
                    return f"Seen: {hours} hours ago"
                elif minutes > 0:
                    return f"Seen: {minutes} minutes ago"
                else:
                    return "Seen Just now"

            lastonline = seen(api['lastSeen'])

            if model.status not in (304, 200):
                image_data = False
            elif model.status in (304, 200):
                image_data = await model.read()

            if stats.status in (400, 404, 204):
                pass

            api = await stats.json()

            def fet(entry):
                js = api[entry]['entries']
                return (js[0]['value'], js[0]['place']) if js else ('0', '0')
            
            def ratio(v1=0, v2=0):
                n1, n2 = int(v1), int(v2)
                if n1 != 0 and n2 != 0:
                    out = n1/n2
                elif n1 != 0 and n2 == 0:
                    out = n1
                elif n1 == 0 and n2 != 0:
                    out = 0
                elif n1 == 0 and n2 == 0:
                    out = 0

                pp = round(out, 2)

                if pp < float(10):
                    output = f"{pp:.2f}"
                elif float(100) > pp >= float(10):
                    output = f"{pp:.1f}"
                elif pp >= float(100):
                    output = str(int(pp))
                
                return output

            def ratio_color(ratio):
                if float(ratio) < float(1):
                    color = 'red'
                elif float(ratio) > float(1):
                    color = 'lime'
                else:
                    color = 'white'
                return color

            # Fetching stats
            wins    = fet('Wins')
            loss    = fet('Losses')
            wlr     = ratio(wins[0], loss[0])
            wlrc    = ratio_color(wlr)

            fkills  = fet('Final kills')
            fdeaths = fet('Final deaths')
            fkdr    = ratio(fkills[0], fdeaths[0])
            fkdrc   = ratio_color(fkdr)

            kills   = fet('Kills')
            deaths  = fet('Deaths')
            kdr     = ratio(kills[0], deaths[0])
            kdrc    = ratio_color(kdr)

            arrows_shot  = fet('Arrows shot')
            arrows_hit   = fet('Arrows hit')
            ahr     = ratio(arrows_shot[0], arrows_hit[0])
            ahrc    = ratio_color(ahr)

            bbreak  = fet('Beds destroyed')
            hws     = fet('Highest winstreak reached')
            games   = fet('Games played') 
            hubs    = (int(games[0])-(int(wins[0])+int(loss[0])))



        final = bwimg(username, rank_color, guild, 'aqua', (f'{gName} ({gTag})'), (f"Level {gLevel} | {gMembers} Members"), (f'Owner: {gOwner}'),
                lastonline, "white",image_data, interval.upper(), "white", gamemode.upper(), "white",
                "lime", wins[0], fkills[0], kills[0], bbreak[0], hws[0], loss[0], fdeaths[0], deaths[0], arrows_shot[0], games[0],
                "aqua", f'(#{wins[1]})', f'(#{fkills[1]})', f'(#{kills[1]})', f'(#{bbreak[1]})', f'(#{hws[1]})',
                        f'(#{loss[1]})', f'(#{fdeaths[1]})', f'(#{deaths[1]})', f'(#{arrows_shot[1]})', f'(#{games[1]})',
                wlr, wlrc, fkdr, fkdrc, kdr, kdrc, ahr, ahrc, level, level_color
                )






        discord_file = discord.File(fp=final, filename="image.png")

        end = time.time()
        taim = (end - start)
        await interaction.edit_original_response(content=f"`Time: {taim:2f}`", attachments=[discord_file])










# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(bedwars(bot))