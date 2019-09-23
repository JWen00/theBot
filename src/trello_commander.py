        # /trello view <ListName> => join the later ones together. 
        # /trello lists
        # /trello newList <NewListName> 
        # /trello deleteList <ListName> 
        # /trello deleteCard <CardName
        # /trello add <cardName> [adds to most recently accessed card, if none]

from src.exceptions.bot_exceptions import InvalidCommandError
from src.exceptions.trello_exceptions import InvalidListNameError


# Assumption: Only one board that we're reading from
class TrelloCommander(): 
    def __init__(self, trelloClient, command, arguement=None, lastAccessed=None): 
        self.client = trelloClient
        self.board = self.client.list_boards()[0]
        self.command = command 
        self.arguement = arguement
        self.lastAccessed = lastAccessed
        self.commands = { 
            "view" : "trelloView",
            "lists" : "trelloLists",
            "newList" : "trelloNewList",
            "deleteList" : "trelloDeleteList", 
            "deleteCard" : "trelloDeleteCard", 
        }

    def run(self): 
        if (self.command not in self.commands): 
            print("Invalid Command Error") 
            raise InvalidCommandError("Error: Command Unknown")

        try: 
            # getattr() can also get just attribute values
            # result = getattr(obj, "method")(args)
            tempObj = TrelloCommander(self.client, self.command)
            result = getattr(tempObj, self.commands[self.command])()
            return result
        except (InvalidListNameError, InvalidCommandError) as e: 
            raise InvalidCommandError("Error: List name not found OR not given") 

    # View the cards of a given list name
    def trelloView(self): 
        listName = self.arguement
        result = []
        result.append("Getting cards for: " + listName) 
        try: 
            cards = self.getList(listName) 
            for card in cards: 
                result.append(card.name) 
            result.append("Fin") 
        except InvalidListNameError as e: 
            result.append(e.message)
        return result
    
    # View the names of all lists in "personal board"
    def trelloLists(self): 
        result = [] 
        result.append("Getting list names...")
        for list in self.board.open_lists(): 
            result.append(list.name)
        result.append("Fin") 
        return result

    # Create a new list
    def trelloNewList(self): 
        newListName = self.arguement
        result = []
        try: 
            l = self.getList(newListName)
            print("List already exists")
            result.add("Error: List already exists")
        except InvalidListNameError as e:    
            self.board.add_list(str(newListName))
            result.append("Successfully added list: " + newListName)
        return result

    # Deletes list from "personal board"
    def trelloDeleteList(self): 
        oldListName = self.arguement
        result = []
        try: 
            l = self.getList(oldListName) 
            self.getList(oldListName).close()
            result.append("Successfully closed list: " + oldListName)
        except InvalidListNameError as e:    
            result.append(e.message) 
        return result
    
    # Deletes the card from the recently accessed list
    def trelloDeleteCard(self): 
        oldCardName = self.arguement
        result = []
        if self.lastAccessed == None: 
            raise InvalidCommandError("Error: Must access list before deleting card from list")
        
        for card in self.getList(self.lastAccessed): 
            if (card.name == oldCardName): 
                card.close() 
                result.append("Successfully deleted " + oldCardName + " from " + self.lastAccessed)
        return result

    def getList(self, listName): 
        openLists = self.board.open_lists(); 
        for l in openLists: 
            if (str(listName).lower() == str(l.name).lower()):
                return l
        raise InvalidListNameError("Error: List name not found")
