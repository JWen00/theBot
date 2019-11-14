from src.bot import Bot
import os
import pickle 

from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path="config/.env", verbose=True)

# Check if session cookies exist 
sessionCookiePath = "config/session_cookies.pickle"
sessionCookie = None
if os.path.exists(sessionCookiePath): 
    with open(sessionCookiePath, 'rb') as cookie: 
        sessionCookie = pickle.load(cookie) 

# Create the bot 
USERNAME = os.getenv("FB_USERNAME")
PASSWORD = os.getenv("FB_PASS")

if not USERNAME or not PASSWORD:
    raise Exception("Username / password not supplied")
if sessionCookie is not None:
    print("Using session cookies to log in")
client = Bot(USERNAME, PASSWORD, session_cookies=sessionCookie)

# Save the session cookies 
session = client.getSession()
with open (sessionCookiePath, 'wb') as cookie: 
    pickle.dump(session, cookie) 

# Listen..
client.listen()  

