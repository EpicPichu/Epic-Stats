from fastapi import FastAPI, HTTPException, Response
import asyncio, aiohttp, sqlite3
import datetime
from main.images import *


app = FastAPI()

connection = sqlite3.connect('names.db')
db = connection.cursor()

@app.get("/")
def read_root():
    return {"Hello": "World"}



# joy bangla




@app.get("/bedwars/{inputname}")
async def bedwalls(inputname: str, interval: str = 'lifetime', mode: str = 'all_modes'):
    async with aiohttp.ClientSession() as session:

        query = db.execute('SELECT * FROM users WHERE lowername = ?', (inputname.lower(),))
        output = query.fetchall()

        if output:
            realname = output[0][1]

        else:
            async with session.get(f'https://stats.pika-network.net/api/profile/{inputname}') as response:

                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="Bad request or resource not found")
                
                api = await response.json()
                realname = api['username']
                
                db.execute("INSERT INTO users (lowername, realname) VALUES (?, ?)", (inputname.lower(), realname))
                connection.commit()

        profilereq = session.get(f'https://stats.pika-network.net/api/profile/{realname}')
        statsreq = session.get(f'https://stats.pika-network.net/api/profile/{realname}/leaderboard?type=BEDWARS&interval={interval}&mode={mode}')
        modelreq = session.get(f"https://starlightskins.lunareclipse.studio/render/custom/"+realname+"/full?wideModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/models/tnt_sit/pose1.obj&slimModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/models/tnt_sit/pose1.obj&propModel=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/models/tnt_sit/pose1prop.obj&propTexture=https://raw.githubusercontent.com/EpicPichu/Epic-Stats/main/assets/models/tnt_sit/tnt.png&cameraPosition={%22x%22:%228.47%22,%22y%22:%2223.06%22,%22z%22:%22-30.87%22}&cameraFocalPoint={%22x%22:%224%22,%22y%22:%2219%22,%22z%22:%22-16.24%22}&cameraFOV=45&cameraWidth=374&cameraHeight=437")

        profile, model, stats = await asyncio.gather(profilereq, modelreq, statsreq)

        if profile.status != 200:
            raise HTTPException(status_code=profile.status, detail="Bad request or resource not found")

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
            raise HTTPException(status_code=stats.status, detail="Bad request or resource not found")

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



    final = bedwars(username, rank_color, guild, 'aqua', (f'{gName} ({gTag})'), (f"Level {gLevel} | {gMembers} Members"), (f'Owner: {gOwner}'),
            lastonline, "white",image_data, interval.upper(), "white", mode.upper(), "white",
            "lime", wins[0], fkills[0], kills[0], bbreak[0], hws[0], loss[0], fdeaths[0], deaths[0], arrows_shot[0], games[0],
            "aqua", f'(#{wins[1]})', f'(#{fkills[1]})', f'(#{kills[1]})', f'(#{bbreak[1]})', f'(#{hws[1]})',
                    f'(#{loss[1]})', f'(#{fdeaths[1]})', f'(#{deaths[1]})', f'(#{arrows_shot[1]})', f'(#{games[1]})',
            wlr, wlrc, fkdr, fkdrc, kdr, kdrc, ahr, ahrc, level, level_color
            )
                
    return Response(final, media_type="image/png")



    return {

        "ign": username,
        "level": level,
        "level_color": level_color,
        "level_bold": level_bold,
        "rank": rank,
        "rank_color": rank_color,
        "friends": friends,
        "guild": guild,
        "gname": gName,
        "gtag": gTag,
        "glevel": gLevel,
        "gmembers": gMembers,
        "gowner": gOwner,
        "last_online": lastonline,

        "stats": {
            "interval": interval,
            "wins": wins[0],
            "losses": loss[0],
            "win_loss_ratio": wlr,
            "win_loss_ratio_color": wlrc,
            
            "fkills": fkills[0],
            "fdeaths": fdeaths[0],
            "final_kill_death_ratio": fkdr,
            "final_kill_death_ratio_color": fkdrc,
            
            "kills": kills[0],
            "deaths": deaths[0],
            "kill_death_ratio": kdr,
            "kill_death_ratio_color": kdrc,
            
            "beds_destroyed": bbreak[0],
            "arrows_shot": arrows_shot[0],
            "arrows_hit": arrows_hit[0],
            "arrow_hit_ratio": ahr,
            "arrow_hit_color": ahrc,
            
            "winstreak": hws[0],
            "games_played": games[0],
            "hubs": hubs
        }
    }



