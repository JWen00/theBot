from src.bot import Bot
from src.env import env
from os import path
import pickle 



# Check if session cookies exist 
session_cookie = None 
if path.exists("session_cookies.pickle"): 
    with open('session_cookies.pickle', 'rb') as cookie: 
        session_cookie = pickle.load(cookie) 

# Create the bot 
client = Bot(env["FB_USERNAME"], env["FB_PASS"], session_cookies=session_cookie)

# Save the session cookies 
session_cookie = client.getSession()
with open ('session_cookie.pickle', 'wb') as cookie: 
    pickle.dump(session_cookie, cookie) 

# Listen..
client.listen()  

