# Fbchat
from fbchat import *
import asyncio 

# Trello 
from .trelloWrapper import TrelloWrapper
 
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

import os.path
import json
import pickle
import re


class Bot(Client):
    def __init__(self):
        super().__init__()

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

    async def on_message(self, mid=None, author_id=None, message_object=None, thread_id=None,
                         thread_type=ThreadType.USER, at=None, metadata=None, msg=None):
                         
        if message_object.text == None: return 
        message_string = str(message_object.text) 
        message_string = message_string.split() 
        command = message_string[0]
        print(f'Got command {command}')

        # Adds chat to activeChats
        if command == "/addChat": await self.addChat(mid, thread_id)

        if thread_id not in self.activeThreads: 
            print("Stuck!")
            return  

        commands = { 
            "/week" :       self.getWeekEvents, 
            "/addEvent" :   self.addEvent,
            "/list" :       self.getList, 
            "/add" :        self.addTolist, 
            "/remove" :     self.removeFromList, 
            "/where" :      self.getCurrentEvent,
            "/help" :       self.sendHelp, 
            "/add" :        self.mentionAll, 
        }

        if command in commands: 
            self.deleteMessages(mid) # Delete the command 

            args = { 
                "message" : message_string[1:], 
                "threadID" : thread_id
            }

            await self.send(
                Message(text=commands[command](args)), 
                thread_id=thread_id, 
                thread_type=thread_type)
            return 

        if message_string in messageMap:
            await self.send_remote_files(messageMap[message_object.text], thread_id=thread_id, thread_type=thread_type)
            return 
        
    async def addChat(self, mid, thread_id): 
        await self.delete_messages([mid]) # Delete the command 
            
        # Update the activeThreads File
        if thread_id not in self.activeThreads: 
            self.activeThreads.append(thread_id)
            print(self.activeThreads)
            try:
                with open("config/active_chats.txt", "a") as f: 
                    f.write(thread_id + "\n") 
            except FileNotFoundError: 
                with open("config/active_chats.txt", "w") as f: 
                    f.write(thread_id + "\n") 
            msg = self.trelloWrapper.processCommand(new, thread_id)

        else:
            print("Thread ID in active threads") 
            msg = ">> This chat is already active!"

        print(msg)
        await self.send(
            Message(text="msg"), 
            thread_id=thread_id, 
            thread_type=thread_type)

        print(f"sent {msg}")
    def mentionAll(self, args): return ">> Function not yet written" 

    def getWeekEvents(self, args): return ">> Function not yet written" 
    
    def addEvent(self, args): return ">> Function not yet written" 
    
    def getList(self, args): return self.trelloWrapper.processCommand("view", args["threadID"]) 
    
    def addTolist(self, args): return self.trelloWrapper.processCommand("add", args)

    def removeFromList(self, args): return self.trelloWrapper(processCommand("remove", args))

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
