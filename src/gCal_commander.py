from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from src.env import env
from src.exceptions.gCal_exceptions import InvalidCalenderNameError
from src.exceptions.bot_exceptions import InvalidCommandError
import json
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Crappy crappy version of NLP.. 
# Want to do this! 
# https://www.analyticsvidhya.com/blog/2017/01/ultimate-guide-to-understand-implement-natural-language-processing-codes-in-python/

class GCal_Commander(): 
    def __init__(self, arguments): 
        self.creds = self.getCredentials() 
        self.client = build('calender', 'v3', credentials=self.creds) 
        self.now = datetime.datetime.utcnow().isoformat() + 'Z'

        self.calenderID_map = None 
        with open("src/calender_map.json", "r") as f: 
            self.calenderID_map = json.loads(f.read()) 

        self.arguements = arguements
        self.commands = { 
            "next" : "getNextEvent",
            "add" : "addEvent", 
            "remove" : "removeEvent", 
            "week" : "getWeeklyEvents",
        }
        
    # Setup Credentials
    def getCredentials(self): 
        creds = None
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

        return creds

    # Parse all the arguments 
    def parseArguements(self): 

        # Has to have at least two words 
        if self.arguements.len() < 2: 
            raise InvalidCommandError("Invalid command: " + " ".join(self.arguements))

        # Pick up keywords 
        command_indicator = self.arguements[0]
        words = [x for x in self.arguements if x is not command_indicator]
        time = getKeywordTime(words) 
        month = getKeywordMonth(words) 
        day = getKeywordDay(words) 
        


        if command_indicator == "next": 
            # Look for a month 
            for word in words: 
                if ()
        elif command_indicator == "add": 
            # calender
            # eventName 
            # DATE/this/next 
            # if (not number): 
            #   get DAY_OF_WEEK   
            #  DateTime can be given in: 
            #  * DATE + MONTH=NONE + START_TIME=NONE
            #  * this +  DAY_OF_WEEK + START_TIME=NONE  
            #  * next +  DAY_OF_WEEK + START_TIME=NONE  
# [word for word in words if word not in noise_list] 
            # By default: 
            #  * MONTH=this_month 
            #  * START_TIME=whole_day 
        elif command_indicator == "remove": 
            return 
        elif command_indicator == "week": 
            return 
        else: 
            raise InvalidCommandError("Command Unknown: " + command_indicator) 
        
    def getKeywordTime(words): 
        for word in words: 
            if word[0] == "@":
                time_str = word[1:]
        
        regexp = re.compile(r"\d:\d{2} ") 
        if regexp.search(time_str): 
            hour = int(time_str[0])
            minute = inttime_str[2:]
            print(hour + ":" + minute) 
        
        

        return 
    
    def getKeywordMonth(words): 
        with open("src/_months.json", "r") as f: 
            _MONTHS = json.loads(f.read()) 
        for word in words: 
            if word in _MONTHS: 
                return _MONTHS.get(word) 
        return None

    def getKeywordDay(words):
        _DAYS_OF_THE_WEEK = None 
        with open("src/_days_of_the_week.json", "r") as f: 
            _DAYS_OF_THE_WEEK = json.loads(f.read()) 
        for word in words: 
            if word in _DAYS_OF_THE_WEEK: 
                return _DAYS_OF_THE_WEEK.get(word) 
            
        return None 

    # def deNoiseWords(words): 
    #     _NOISE_WORDS = ["a", "any", "at", "as", "the", "my", "are", "when", "so", "of", "there", "his", "is", "it", "if"]
    #     return 

    def run(self): 

        # Check calender validity
        if calenderName in calenderID_map: 
            calenderID = self.calenderID_map.get(calenderName) 
        else: 
            raise InvalidCalenderNameError("Calender Name Unknown: " + calenderName)

      

    # Get the next event given a particular calender
    def getNextEvent(self, calenderName):
        

        # Get event 
        result = []
        events = self.client.events().list(calendarId=calenderID, timeMin=self.now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    # Adds an event to a calender
    def addEvent(self, calender, newEventName, eventPeriod=None, wholeDayEvent=True): 
        # insert(calendarId=*, body=*)
        return 

    # Removes an event given a calender
    def removeEvent(self, calender, oldEventName): 
        return 

    # Obtains a summary of this week's events [Not including UNSW calender] 
    def getWeeklyEvents(self): 
        return
