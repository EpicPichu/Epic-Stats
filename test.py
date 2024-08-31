import sqlite3
from fastapi import FastAPI, HTTPException
import aiohttp

conn = sqlite3.connect('names.db')
db = conn.cursor()



app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/bedwars/{ign}")
async def bedwalls(ign: str):



    query = db.execute('SELECT * FROM users WHERE lowername = ?', (ign.lower(),))
    t1 = query.fetchall()

    if t1:
        return t1[0][1]
    
    else:

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://stats.pika-network.net/api/profile/{ign}') as response:

                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="Bad request or resource not found")
                
                api = await response.json()
                
                db.execute("INSERT INTO users (lowername, realname) VALUES (?, ?)", (ign.lower(), api['username']))
                conn.commit()

                return api['username']