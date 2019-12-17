from trello import TrelloClient 
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path="../config/.env", verbose=True)


# client.list_boards() => Gets list of boards
# board.open_lists() => Get lists in board 

# Honestly, py-trello has awful documentation and I had to look at their test code to understand how to use it :(
 
class TrelloWrapper(): 
    def __init__(self): 
        self.client = TrelloClient( 
            api_key=os.getenv("TRELLO_API_KEY"), 
            api_secret=os.getenv("TRELLO_SECRET_KEY"), 
            token=os.getenv("TRELLO_TOKEN") 
        )

        self.board = self.client.list_boards()[0]
        self.lists = self.board.open_lists() 

    def processCommand(self, command, args): 
        """ Directs the command to their corresponding method """

        commandMap = { 
            "new" : self.createNewList,
            "view" : self.trelloView,
            "add" : self.trelloAddCard, 
            "remove" : self.trelloDeleteCard, 
        }

        if command not in commandMap: return ">> Command not found" 
        
        return commandMap[command](args)

    def getListByID(self, listID): 
        """ Gets a list OBJ by their ID """
        for l in self.lists: 
            if l.name == listID: 
                return l 
        
        return None

    def createNewList(self, args): 
        """ Create a new list on board, cannot repeat """ 
        print(args)
        listID = args["thread_id"]
        print(listID) 
        for l in self.lists: 
            print("Comparing with " + l.name)
            if l.name == listID: 
                return ">> This chat is already added!"
        self.board.add_list(str(listID)) 
        return ">> Now listening to this chat!"

    def trelloView(self, args): 
        """ View the cards of given list """

        l = self.getListByID(args["threadID"] ) 

        result = ""
        for card in l: result.append(f' * {card.name}\n')
        return result 
    
    def trelloAddCard(self, args): 
        """ Addes a card in a list """ 

        listID = args["threadID"] 
        cardName = args["message"] 

        l = self.getListByID(listID) 
        l.append(cardName) # Check this 
        
    
    def trelloDeleteCard(self, args): 
        """ Deletes an item from a list """ 

        args = args.split(" ")
        if len(args) < 2: return ">> Missing arguments"  

        listID = args[0] 
        if not doesListExist(listID): return ">> This list does not exist"

        cardName = args[1:] 

        for l in self.lists: 
            if l.name == listID: 
                for card in l: 
                    if card.name == cardName:
                        card.close() 
                        return ">> Deleted item!" 
        
        return ">> Item doesn't exist"

