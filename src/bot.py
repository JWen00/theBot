# Fbchat
from fbchat import Client
from fbchat.models import *

# Trello 
from .trelloWrapper import TrelloWrapper



# Google Calender 
from .gCal_commander import GCal_Commander
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Others 
import os.path
import json
import pickle
import re


class Bot(Client):
    def __init__(self, email, password, **kwargs):
        # user_agent=None, max_tries=5, session_cookies=None, logging_level=20 
        super().__init__(email, password, **kwargs)
        self.botID = self.getSession()["c_user"]

        self.gCalCredentials = self.getGCalCredentials()
        self.gCalClient = build('calendar', 'v3', credentials=self.gCalCredentials)

        self.lastAccessedTrelloList = None

    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):

        # Only works in non-group settings && text messages
        if message_object.text == None or thread_type != ThreadType.USER:
            return 

        message_string = str(message_object.text)
        # print("ThreadID = " + thread_id)
        # print("AuthurID = " + author_id) 

        # Delete messages starting with '/' 
        if message_string[0][0] == "/": 
            self.deleteMessages(mid)

        messageMap = None  
        with open("config/msg_reactions.json", "r") as fp: 
            messageMap = json.load(fp) 
        if message_string in messageMap:
            self.deleteMessages(mid)
            if author_id == self.uid:
                self.sendLocalFiles(messageMap[message_object.text], thread_id=thread_id, thread_type=ThreadType.USER)
            
        # Commands sent to self
        if thread_id == self.botID:
            message_string = message_string.lower() 
            message_string = message_string.split() 

            # Error Checking before we try to run commands
            checkingMessage, status = self.checkCommand(message_string)
            self.sendMessage(checkingMessage, thread_id=thread_id, thread_type=ThreadType.USER)

            commandData = self.handleCommand(message_string) 
            self.sendMessage(commandData, thread_id=thread_id, thread_type=ThreadType.USER)

         
            
    def getGCalCredentials(self): 
        creds = None

        try:
            with open('config/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        except Exception:
            pass

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('config/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

        return creds

    def manageTrelloCommand(self, msg):
        command = msg[0] 
        argument = msg[1] if len(msg) > 1 else None
        return_message = []
        print("Running trello API...") 
        trelloCommander = TrelloCommander(self.trelloClient, command, argument, self.lastAccessedTrelloList)
        return_message = trelloCommander.run() 

        if command == "view" : 
            lastAccessedTrelloList = argument
        return return_message
   
    def manageCalenderCommand(self, msg): 
        command = msg[0] 
        arguments = [x for x in msg if x is not command]
        return_message = []
        print("Running Google Calender API...")
        gCalCommander = GCal_Commander(self.gCalClient, arguments)
        gCalCommander.run()
        return return_message
    
    def checkCommand(self, command): 
        apiTarget = command[0] 
        arguments = command[1:]

        # Check api target exists
        if apiTarget != "/cal" or apiTarget != "/trello": 
            return ("Unknown API called", False)

        # Get Success Message 
        if apiTarget == "/cal": 
            return_message = "Running gCal Command: " + arguments[0] 
            return (return_message, True) 
        
        elif apiTarget == "/trello": 
            return_message = "Running Trello Command: " + arguments[0] 
            return (return_message, True) 
    
    def handleCommand(self, command): 
        try:
            if command == "/trello": 
                return self.manageTrelloCommand(command)

            elif command == "/cal": 
                return self.manageCalenderCommand(command)
            
        except (InvalidCommandError, InvalidListNameError) as e: 
            return e.args[0]

    