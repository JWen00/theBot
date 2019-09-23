from trello_handler import TrelloHandler
from trello_exceptions import * 
import pytest 

@pytest.fixture 
def handler(): 
    handler = TrelloHandler()
    return handler

def test_getList_working(handler): 
    l = handler.getList("food places to visit")
    # assert l == "5d59fe1048e80e897111a920"
    
def test_getList_error(handler): 
    with pytest.raises(InvalidListNameError):
        l = handler.getList("RANDOM TEXT")


def test_addCardToList(handler): 
    handler.addCardToList("testing1", "food places to visit")


def test_getListCards(handler): 
    cardList = handler.getListCards("food places to visit") 
    print(cardList) 