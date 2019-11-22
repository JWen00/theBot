from trello import TrelloClient 

# Assumption: Only one board that we're reading from
class TrelloWrapper(): 
    def __init__(self): 
        self.client = TrelloClient( 
            api_key=os.getenv("TRELLO_API_KEY"), 
            api_secret=os.getenv("TRELLO_SECRET_KEY") 
            token=os.getenv("TRELLO_TOKEN") 
        )

        self.board = self.client.list_boards[0]
        self.lists = self.board.open_lists() 


    def processCommand(self, command, args): 

        commandMap = { 
            "new" : self.createNewList,
            "view" : self.trelloView,
            "remove" : self.trelloDeleteCard, 
        }

        if command not in commandMap: return ">> Command not found" 
        
        return commandMap[command](args)

    def doesListExist(listID): 
        for l in self.lists: 
            if l.name == listID: return True
        return False

    def createNewList(self, listID): 
        """ Create a new list on board, cannot repeat """ 

        # List exists aready
        if self.doesListExist(listID): return ">> This list already exists"
        
        self.board.add_list(str(listID)) 
        return ">> Added new list!" 

    def trelloView(self, listID): 
        """ View the cards of given list """

        if not self.doesListExist(listID): return ">> This list does not exist"

        result = ""
        for l in self.lists: 
            if l.name == listID: 
                for card in l: 
                    result.append(f' * {card.name}\n')
                return result 
    
    
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

