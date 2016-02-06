class Card:
    def __init__(self,suit,num):
        self.suit = suit
        self.num=num

    def getSuit():
        return self.suit

    def getNum():
        return self.num

class Hands:
    def __init__(self,cards):
        if len(cards) == 5:
            self.cards=cards
        else:
            return False

    def getHand():
        hand = " "
        return hand

    def getChangeFlag():
        change = judgeHand()
        return change

    def judgeHand():
        return (1,0,1,1,0)

class Game(Hands):
    def __init__(self,cards,status):
        Hands.__init__(self,cards)
        self.library=cards
        self.status = 0
        return self.cards

    def changeHands(cards):
        self.library.append(newCards(self.cards,cards))
        self.cards=cards
        return self.cards

    def newCards(card1,card2):
        list(set(b)-set(a))
