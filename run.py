from src.bot import Bot
import os
import pickle 
import asyncio
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path="config/.env")


loop = asyncio.get_event_loop()

async def start(): 
    USERNAME = os.getenv("FB_USERNAME")
    PASSWORD = os.getenv("FB_PASS") 
    if not USERNAME or not PASSWORD: raise Exception("Username / password not supplied")

    sessionCookiePath = "config/session_cookies.pickle"
    sessionCookie = None
    if os.path.exists(sessionCookiePath): 
        with open(sessionCookiePath, 'rb') as cookie: 
            sessionCookie = pickle.load(cookie) 


    print(f'Logging into {USERNAME}...')
    bot = Bot() 
    await bot.start(USERNAME, PASSWORD, session_cookies=sessionCookie)

    if sessionCookie is not None: 
        print("Using session cookies to log in")
    else: 
        print("Saved session cookies") 
        session = client.getSession()
        with open (sessionCookiePath, 'wb') as cookie: 
            pickle.dump(session, cookie) 

    print("Logged in!")
    bot.listen() 

loop.run_until_complete(start()) 
loop.run_forever() 


