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
            "add" : self.trelloAddCard, 
            "remove" : self.trelloDeleteCard, 
        }

        if command not in commandMap: return ">> Command not found" 
        
        return commandMap[command](args)



    def getListByID(self, listID): 
        for l in self.lists: 
            if l.name == listID: 
                return l 
        
        return None

    def createNewList(self, listID): 
        """ Create a new list on board, cannot repeat """ 
        
        self.board.add_list(str(listID)) 

    def trelloView(self, listID): 
        """ View the cards of given list """

        l = self.getListByID(listID) 

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

