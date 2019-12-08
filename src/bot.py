# Fbchat
from fbchat import Client
from fbchat.models import *

# Trello 
from .trelloWrapper import TrelloWrapper

# # Google Calender 
# from .gCal_commander import GCal_Commander
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

import os.path
import json
import pickle
import re


class Bot(Client):
    def __init__(self, email, password, **kwargs):
        # user_agent=None, max_tries=5, session_cookies=None, logging_level=20 
        super().__init__(email, password, **kwargs)
        # self.botID = self.getSession()["c_user"] # TODO: Deal with session things later 

        self._trello = TrelloWrapper() 
        # self._gCalCredentials = self.getGCalCredentials()
        # self._gCalClient = build('calendar', 'v3', credentials=self.gCalCredentials)

        try: 
            self._msgReactions = {}
            with open("config/msg_reactions.json", "r") as f: 
                self._msgReactions = json.load(f) 

            self.activeThreads = []
            with open("config/active_chats.txt") as f: 
                self.activeThreads = f.read().splitlines() 

        except FileNotFoundError: 
            pass 

    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):

        if message_object.text == None: return 

        message_string = str(message_object.text) 
        message_string = message_string.lower() 
        message_string = message_string.split() 
        command = message_string[0]
        if command == "/addChat": 
            self.activeThreads.append(thread_id)  
            self.trelloWrapper.processCommand(new, thread_id)
            self.sendMessage(">> JenniBot now works in this chat!", thread_id=thread_id, thread_type=ThreadType.USER)
            return

        if thread_id not in self.activeThreads: return 

        commands = { 
            "/week" : self.getWeekEvents, 
            "/addEvent" : self.addEvent,
            "/list" : self.getList, 
            "/add" : self.addTolist, 
            "/remove" : self.removeFromList, 
            "/where" : self.getCurrentEvent,
            "/help" : self.sendHelp, 
        }

        if command in commands: 
            self.deleteMessages(mid) # Delete the command 

            args = { 
                "message" : message_string[1:], 
                "threadID" : thread_id
            }

            self.sendMessage(commands[command](args), thread_id=thread_id, thread_type=ThreadType.USER)
            return 

        if message_string in messageMap:
            self.sendLocalFiles(messageMap[message_object.text], thread_id=thread_id, thread_type=ThreadType.USER)
            return 
        
    def getWeekEvents(self, args): return ">> Function not yet written" 
    
    def addEvent(self, args): return ">> Function not yet written" 
    
    def getList(self, args): return self.trelloWrapper.processCommand("view", args["threadID"]) 
    
    def addTolist(self, args): return self.trelloWrapper.processCommand("add", args)

    def removeFromList(self, args): return self.trelloWrapper(processCommand("remove", args)

    def getCurrentEvent(self, args): return ">> Function not yet written" 
    
    def sendHelp(self, args): return "Commands:\n /week\n /addEvent\n /list\n /remove\n /where\n" 


    # def getGCalCredentials(self): 
    #     creds = None

    #     try:
    #         with open('config/token.pickle', 'rb') as token:
    #             creds = pickle.load(token)
    #     except Exception:
    #         pass

    #     # If there are no (valid) credentials available, let the user log in.
    #     if not creds or not creds.valid:
    #         if creds and creds.expired and creds.refresh_token:
    #             creds.refresh(Request())
    #         else:
    #             flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
    #             creds = flow.run_local_server(port=0)

    #     # Save the credentials for the next run
    #     with open('config/token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)

    #     return creds
