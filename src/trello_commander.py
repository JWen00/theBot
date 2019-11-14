        # /trello view <ListName> => join the later ones together. 
        # /trello lists
        # /trello newList <NewListName> 
        # /trello deleteList <ListName> 
        # /trello deleteCard <CardName
        # /trello add <cardName> [adds to most recently accessed card, if none]

from .exceptions import InvalidCommandError, InvalidListNameError

# Assumption: Only one board that we're reading from
class TrelloCommander(): 
    def __init__(self, trelloClient, command, argument=None, lastAccessed=None): 
        self.client = trelloClient
        self.board = self.client.list_boards()[0]
        self.command = command 
        self.argument = argument
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
            raise InvalidCommandError("Error: Command Unknown")
        return getattr(self, self.commands[self.command])()

    # View the cards of a given list name
    def trelloView(self): 
        listName = self.argument
        result = []
        result.append("Cards for: " + listName) 
        cards = self.getList(listName) 
        for card in cards: 
            result.append(card.name) 
        result = "\n".join(result) 
        return result
    
    # View the names of all lists in "personal board"
    def trelloLists(self): 
        result = [] 
        result.append("All list names...")
        for list in self.board.open_lists(): 
            result.append(list.name)
        result = "\n".join(result) 
        return result

    # Create a new list
    def trelloNewList(self): 
        newListName = self.argument
        result = []
        try: 
            l = self.getList(newListName)
            print("List already exists")
            result.add("Error: List already exists")
        except InvalidListNameError as e:    
            self.board.add_list(str(newListName))
            result.append("Successfully added list: " + newListName)

        result = "\n".join(result) 
        return result

    # Deletes list from "personal board"
    def trelloDeleteList(self): 
        oldListName = self.argument
        result = []
        try: 
            l = self.getList(oldListName) 
            self.getList(oldListName).close()
            result.append("Successfully closed list: " + oldListName)
        except InvalidListNameError as e:    
            result.append(e.args[0]) 
        return result
    
    # Deletes the card from the recently accessed list
    def trelloDeleteCard(self): 
        oldCardName = self.argument
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
