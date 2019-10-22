
from datetime import date, datetime
import calendar
import os.path

from src.env import env
from src.fakeNLP import FakeNLP
from src.exceptions.gCal_exceptions import InvalidCalenderNameError
from src.exceptions.bot_exceptions import InvalidCommandError
import json



# Crappy crappy version of NLP.. 
# Want to do th
# is! https://www.analyticsvidhya.com/blog/2017/01/ultimate-guide-to-understand-implement-natural-language-processing-codes-in-python/

class GCal_Commander(): 
    def __init__(self, gCalClient, arguments): 
        self.client = gCalClient
        self.now = date.today()
        self.fakeNLP = FakeNLP()
        # ===
        self.calenderID_map = None 
        with open("config/calenderID_map.json", "r") as f: 
            self.calenderID_map = json.loads(f.read()) 
        
        self.arguments = arguments
        self.commands = { 
            "next" : "getNextEvent",
            "add" : "addEvent", 
            "week" : "getWeeklyEvents",
            # "remove" : "removeEvent",  # TODO: Think about this later 
        }

    def run(self): 

        # Has to have at least two words 
        if len(self.arguments) < 2: 
            command = " ".join(self.arguments)
            raise InvalidCommandError("Invalid command: " + command)

        command_indicator = self.arguments[0]
        if command_indicator not in self.commands: 
            raise InvalidCommandError("Error: Command " + command_indicator + " not found") 
       
        # Grab all keywords
        words = [x for x in self.arguments if x is not command_indicator]
        keywords = {} 
        keywords["time"] = self.fakeNLP.getKeywordTime(words) 
        keywords["date"] = self.fakeNLP.getKeywordDate(words) 
        keywords["month"] = self.fakeNLP.getKeywordMonth(words) 
        keywords["day"] = self.fakeNLP.getKeywordDay(words) 
        keywords["week"] = self.fakeNLP.getKeywordWeek(words) 
        keywords["eventType"] = self.fakeNLP.getKeywordEventType(words) 
        # TODO: Improve getEventName 
        keywords["eventName"] = words[1] 
        
        # Run the associated command
        return getattr(self, self.commands[command_indicator])(keywords)
      

    # Get the next event given a particular calender
    def getNextEvent(self, keywords):
        return_msg = []
        calenderID = self.calenderID_map.get(keywords.get("eventType")) 
        event_results = self.client.events().list(calendarId=calenderID, timeMin=self.now, maxResults=1, singleEvents=True, orderBy="startTime").execute() 
        nextEvent = event_results["items"] 

        # Format: {Event Name} on {if not today: day_of_week} {if startTime available: @startTime}
        if nextEvent: 
            eventDate = nextEvent["start"].get("date") 
            eventDateTime = nextEvent["start"].get("dateTime") 
            
            format_string = keywords.get("eventName")
            if eventDate != self.now: 
                day_of_nextEvent =  calendar.day_name[eventDate.weekday()]
            
            # For now, find out what startTime is!! 
            # If the event is today, get the start time
            # if nextEvent["start"].get("dateTime") == None: 
               
            return_msg.append("dateTime: " + eventDateTime)    
            return_msg.append(format_string)
            return return_msg

        return_msg.append("No upcoming " + keywords.get("eventType") + " found.") 
        return return_msg


    def addEvent(self, keywords): 

        # Check if we have a valid eventType
        if not (keywords.get("eventType") == "shift" or keywords.get("eventType") == "event"): 
            return "Error: Calender not specified" 

        # Get the yyyy-mm-dd string 
        yearMonthDate_string = self.getDateMonthTimeString(keywords) 

        # Get the time/AllDayEvent
        # TODO: Eventually add in time..
        # allDayEvent = False
        # if keywords.get("time") == None:
        #     allDayEvent = True 
    
        # Get the calender ID 
        calenderID = self.calenderID_map().get(keywords.get("eventType")) 
        self.addEvent(date)

        # Make request object 
        req_obj = { 
            "summary" : keywords.get("eventName") + keywords.get("time"), 
            "start" : { 
                "date" : yearMonthDate_string
            }, 
            "end" : { 
                "date" : yearMonthDate_string
            }
        }

        event = self.client.events().insert(calendarId=calenderID, body=req_obj).execute()
        result = []
        return "Successfully added event: " + keywords.get("eventName") + " " + keywords.get("time") + " on " + yearMonthDate_string[0:2] + "/" + yearMonthDate_string[3:5] + "/" + yearMonthDate_string[6:10]

    # Removes an event given a calender
    # def removeEvent(self, keywords): 
    #     return 

    # Obtains a summary of this week's events [in EVENTS calender]
    def getWeeklyEvents(self, keywords):  
        calenderID = self.calenderID_map.get("events") 
        timeMin = self.now 
        timeMax = self.now + datetime.timedelta(days=7)
        events = self.client.events().list(calendarId=calenderID, timeMin=timeMinm, timeMax=timeMax, singleEvents=True, orderBy="startTime")

        return_msg = ["Events in the next week: \n"]
        for event in events["items"]: 
            return_msg.append(event["summary"] + "on" + event["start"].get("date") + "\n")
        return_msg.append("Fin\n") 
        return return_msg

    def getKeywordEventType(words): 

        # Note: Since there's only 3, I'm not storing it, but can potentially store this too. 
        eventTypes = ["class", "event", "shift"] 
        for word in words: 
            if word in eventTypes: 
                return word 
        
        return None 

    def getDateMonthYearString(self, keywords): 

        date = "" 
        month = ""
        year = ""

        # CASE_ONE: (+month) +date (+time) 
        if keywords.get("date") != None:
            date = keywords.get("date") 
            year = self.now.year
            if date < 0 or date > 31: 
                date = (self.now + datetime.timedelta(days=1)).day

            if keywords.get("month") == None: 
                if date == "01": 
                    month = int(keywords.get("month")) + 1 
                    month = str(month) 
                month = keywords.get("month") 
            else: 
                month = keywords.get("month")
            

        # CASE_TWO: +this/next + weekday 
        elif keywords.get("week") != None and keywords.get("day") != None:
            days_difference = int(keywords.get("day")) - int(self.now.day) 
            new_date = None
            if keywords.get("week") == "this": 
                new_date = self.now + datetime.timedelta(days=days_difference)
            elif keywords.get("week") == "next": 
                days_difference += 7
                new_date = self.now + datetime.timedelta(days=days_difference)

            day = str(new_date.today)
            month = str(new_date.month) 

        else: 
            tomorrow = self.now + datetime.timedelta(days=1) 
            date = str(tomorrow.day)
            month = str(tomorrow.month) 
            year = str(tomorrow.year)

        # Get the string to pass into the request 
        yearMonthDate_string = year + "-" + month + "-" + date