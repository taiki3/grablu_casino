# -*- coding: utf-8 -*-

from Autocasino import pokerjJudgeHand

class CardInfo:
    def __init__(self):
        self.suit = ""
        self.num = 0

    def setCardInfo(self, suit, num):
        self.suit = suit
        self.num = num
    def getSuit(self):
        return self.suit
    def setSuit(self, suit):
        self.suit = suit
    def getNum(self):
        return self.num
    def setNum(self, num):
        self.num = num

hands = {1:CardInfo(),2:CardInfo(),3:CardInfo(),4:CardInfo(),5:CardInfo()}
hands[1].setCardInfo('d', 6)
hands[2].setCardInfo('d', 6)
hands[3].setCardInfo('d', 4)
hands[4].setCardInfo('d', 99)
hands[5].setCardInfo('d', 6)

handPattern, holdPos = pokerjJudgeHand.judgeHand(hands) # return( 手役パターン, ホールドする場所(Φ,Φ,Φ,Φ,Φ) )
if __name__ == '__main__':
    if(handPattern==1):
        print "+ロイヤルストレートフラッシュ+"
        print holdPos
    elif(handPattern==2):
        print "+ファイブカード+"
        print holdPos
    elif(handPattern==3):
        print "+ストレートフラッシュ+"
        print holdPos
    elif(handPattern==4):
        print "+フォーカード+"
        print holdPos
    elif(handPattern==5):
        print "+フルハウス+"
        print holdPos
    elif(handPattern==6):
        print "+ロイヤル4枚残し+"
        print holdPos
    elif(handPattern==7):
        print "+フラッシュ+"
        print holdPos
    elif(handPattern==8):
        print "+3カード+"
        print holdPos
    elif(handPattern==9):
        print "+ストレート+"
        print holdPos
    elif(handPattern==10):
        print "+2ペア+"
        print holdPos
    elif(handPattern==11):
        print "+ストレートフラッシュ4枚残し+"
        print holdPos
    elif(handPattern==12):
        print "+ロイヤル3枚残し+"
        print holdPos
    elif(handPattern==13):
        print "+ストレート4枚残し+"
        print holdPos
    elif(handPattern==14):
        print "+1ペア+"
        print holdPos
    elif(handPattern==15):
        print "+ストフラ3枚残し+"
        print holdPos
    elif(handPattern==16):
        print "+ロイヤル2枚残し+"
        print holdPos
    elif(handPattern==17):
        print "+ストレート3枚残し+"
        print holdPos
    elif(handPattern==18):
        print "+フラッシュ4枚残し+"
        print holdPos
    elif(handPattern==19):
        print "+ストフラ2枚残し+"
        print holdPos
    elif(handPattern==20):
        print "+ストレート2枚残し+"
        print holdPos
    elif(handPattern==21):
        print "+フラッシュ3枚残し+"
        print holdPos
    else:
        print "+全チェンジ+"
        print holdPos