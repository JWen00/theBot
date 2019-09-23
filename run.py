# -*- coding: UTF-8 -*-

from fbchat import Client
from fbchat.models import *
from trello import TrelloClient 
from src.trello_commander import TrelloCommander
from src.exceptions.trello_exceptions import InvalidListNameError
from src.exceptions.bot_exceptions import InvalidCommandError
import os
import os.path
import json
from src.env import env


class Bot(Client):
    def __init__(self, email, password, user_agent=None, max_tries=5, session_cookies=None, logging_level=20): 
        super().__init__(email, password, user_agent=None, max_tries=5, session_cookies=None, logging_level=20)
        self.trelloClient = TrelloClient( 
            api_key=env["TRELLO_API_KEY"],
            api_secret=env["TRELLO_SECRET_KEY"],
            token=env["TRELLO_TOKEN"],
            )
        self.lastAccessedList = None

    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):

        # Only responsive to text messages
        # Only works in non-group settings 
        if message_object.text == None or thread_type != ThreadType.USER:
            return 

        message_string = str(message_object.text)
        # print("ThreadID = " + thread_id)
        # print("AuthurID = " + author_id) 

        # Delete messages starting with '/' 
        if message_string[0][0] == "/": 
            self.deleteMessages(mid)

        # Commands sent to self
        if thread_id == env["THREAD_ID_SELF"]: 
            msg = message_string.split() 
            api_indicator = msg[0]
            command = [x for x in msg if x is not api_indicator]
            return_message = []
            if api_indicator == "/trello": 
                try: 
                    return_message = self.manageTrelloCommand(command)
                except InvalidCommandError as e: 
                    self.sendMessage(e.message, thread_id=thread_id, thread_type=ThreadType.USER) 
            elif api_indicator == "/cal": 
                try: 
                    return_message = self.manageCalenderCommand(command)
                except InvalidCommandError as e: 
                    self.sendMessage(e.message, thread_id=thread_id, thread_type=ThreadType.USER) 

            # Convert message from list into an entire string 
            block_reply = "\n".join(return_message) 
            self.sendMessage(block_reply, thread_id=thread_id, thread_type=ThreadType.USER)

        # Initial Information
        messageMap = None  
        

        # If messaage require react 
        if message_string in messageMap:
            self.deleteMessages(mid)
            if author_id == self.uid:
                print(messageMap[message_object.text])
                self.sendLocalFiles(messageMap[message_object.text], thread_id=thread_id, thread_type=ThreadType.USER)
        
    # /trello view <ListName>
    # /trello lists
    # /trello newList <NewListName> 
    # /trello deleteList <ListName> 
    # /trello deleteCard <CardName>
    # /trello add <cardName> [adds to most recently accessed card, if none]
    
    def manageTrelloCommand(self, msg):
        command = msg[0] 
        arguement = msg[1] if len(msg) > 1 else None
        return_message = []
        try: 
            print("Running...") 
            trelloCommander = TrelloCommander(self.trelloClient, command, arguement, self.lastAccessedList)
            return_message = trelloCommander.run() 
            if command == "view" : lastAccessedList = arguement
            return return_message
        except InvalidCommandError as e: 
            raise InvalidCommandError(e.message)
        

    def manageCalenderCommand(self, msg): 
        command = msg[0] 
        arguement = msg[1] if len(msg) > 1 else None
        return_message = []
        try: 
            print("Running...")
            return return_message

        except InvalidCommandError as e: 
            raise InvalidCommandError(e.message)

client = Bot(env["FB_USERNAME"], env["FB_PASS"])
session_cookies = client.getSession()
client.listen()  

