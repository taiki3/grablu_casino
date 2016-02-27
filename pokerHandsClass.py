# -*- coding: utf-8 -*-
from collections import Counter

class Card:
    def __init__(self):
        self.suit = u''
        self.num = 0

    def setCard(self,suit,num):
        self.suit = suit
        self.num = num
        return self

    def getCard(self):
        return self

    def showSuit(self):
        return str(self.suit)

    def showNum(self):
        return str(self.num)

    def showCard(self):
        return str( self.suit+str(self.num) )

    def showCardStr(self):
        if( self.suit == u'99' or self.num == 99):
            return u'Jo'

        suit = ""
        if( self.suit == u's'):
            suit = u'♠'
        elif( self.suit == u'h'):
            suit = u'♡'
        elif( self.suit == u'd'):
            suit = u'♢'
        elif( self.suit == u'c'):
            suit = u'♣'

        return suit+str(self.num)

class Hands:
    def __init__(self):
        self.cardList = [Card(),Card(),Card(),Card(),Card()]
        self.handPattern = False
        self.holdPos = False

    def setHands(self,cards):
        assert type(cards) == list
        assert len(cards) == 5
        cardList = []
        for i in [0,1,2,3,4]:
            cardList.append( cards[i] )
        self.cardList = cardList

    def showHoldHandPos(self,isRedoJudge):
        # isRedoJudge ジャッジ関数を呼び直すか否か
        if(isRedoJudge):
            handPattern,holdPos = self.judgeHand()
            self.handPattern = handPattern
            self.holdPos = holdPos
            return self.holdPos
        elif(not self.holdPos):
            return False
        else:
            return self.holdPos

    def showHoldHandPosStr(self,isRedoJudge):
        holdPos = self.showHoldHandPos(isRedoJudge)
        strHoldPos = u""
        for i in [0,1,2,3,4]:
            if( holdPos[i] ):
                strHoldPos += u'YES '
            else:
                strHoldPos += u'NO '
        return strHoldPos

    def showHandKeepingReason(self,isRedoJudge):
        # isRedoJudge ジャッジ関数を呼び直すか否か
        if(isRedoJudge):
            handPattern,holdPos = self.judgeHand()
            self.handPattern = handPattern
            self.holdPos = holdPos
        else:
            pass

        if(self.handPattern==1):
            return u"+ロイヤルストレートフラッシュ+"
        elif(self.handPattern==2):
            return u"+ファイブカード+"
        elif(self.handPattern==3):
            return u"+ストレートフラッシュ+"
        elif(self.handPattern==4):
            return u"+フォーカード+"
        elif(self.handPattern==5):
            return u"+フルハウス+"
        elif(self.handPattern==6):
            return u"+ロイヤル4枚残し+"
        elif(self.handPattern==7):
            return u"+フラッシュ+"
        elif(self.handPattern==8):
            return u"+ストレート+"
        elif(self.handPattern==9):
            return u"+スリーカード+"
        elif(self.handPattern==10):
            return u"+ツーペア+"
        elif(self.handPattern==11):
            return u"+ストレートフラッシュ4枚残し+"
        elif(self.handPattern==12):
            return u"+ロイヤル3枚残し+"
        elif(self.handPattern==13):
            return u"+ストレート4枚残し+"
        elif(self.handPattern==14):
            return u"+ワンペア+"
        elif(self.handPattern==15):
            return u"+ストフラ3枚残し+"
        elif(self.handPattern==16):
            return u"+ロイヤル2枚残し+"
        elif(self.handPattern==17):
            return u"+ストレート3枚残し+"
        elif(self.handPattern==18):
            return u"+フラッシュ4枚残し+"
        elif(self.handPattern==19):
            return u"+ストフラ2枚残し+"
        elif(self.handPattern==20):
            return u"+ストレート2枚残し+"
        elif(self.handPattern==21):
            return u"+フラッシュ3枚残し+"
        else:
            return u"+全チェンジ+"

    def showCards(self):
        cards= []
        for i in [0,1,2,3,4]:
            cards.append( self.cardList[i].suit+str(self.cardList[i].num) )
        return cards

    def showCardsStr(self):
        strCards = u""
        for i in [0,1,2,3,4]:
            suit = ""
            if( self.cardList[i].suit == u'99' or self.cardList[i].num == 99):
                strCards += u'Jo '
                continue
            if( self.cardList[i].suit == u's'):
                suit = u'♠'
            elif( self.cardList[i].suit == u'h'):
                suit = u'♡'
            elif( self.cardList[i].suit == u'd'):
                suit = u'♢'
            elif( self.cardList[i].suit == u'c'):
                suit = u'♣'
            strCards += suit + str(self.cardList[i].num) + u" "
        return strCards

    def _countSuitFromHands(self):
        ## ハンドにそのスートがいくつ含まれているか
        ### example
        # countList['s':1,'d':1,'c':2,'99':1]
        countDict = {}
        for card in self.cardList:
            if( countDict.has_key(card.suit) ):
                countDict[card.suit] +=1
            else:
                countDict[card.suit] = 1
        return countDict

    def _countNumFromHands(self):
        ## ハンドにその数字がいくつ含まれているか
        ### example
        # countList[12:1,2:1,3:2,99:1]
        countDict = {}
        for card in self.cardList:
            if( countDict.has_key(card.num) ):
                countDict[card.num] +=1
            else:
                countDict[card.num] = 1
        return countDict

    def _isExistJoker(self):
        for card in self.cardList:
            if (card.suit==u'99' or card.num == 99):
                return True
        else:
            return False

    def _posExistJoker(self):
        for i in xrange(len(self.cardList)):
            if (self.cardList[i].suit==u'99' or self.cardList[i].num == 99):
                return i
        else:
            return False

    def _isPosJoker(self,pos):
        #iの位置にjokerはいるか
        if( self.cardList[pos].suit ==u'99' or self.cardList[pos].num == 99):
            return True
        return False

    def _isExistSuit(self,suit):
        for card in self.cardList:
            if (card.suit==suit):
                return True
        else:
            return False

    def _isExistNum(self,num):
        for card in self.cardList:
            if (card.num==num):
                return True
        else:
            return False

    def _countFromStraightList(self,straitList):
        #ハンドにリストの中のカードが何枚あるか
        countStraightCard = 0
        if( self._isExistJoker() ):
            countStraightCard+=1

        overLapList = []
        for card in self.cardList:
            for j in straitList:
                if( (not card.num in overLapList) and\
                  card.num == j):
                    overLapList.append(j)
                    countStraightCard+=1
        return countStraightCard

    def _holdHandFromPare(self):
        holdCardList = [False,False,False,False,False]
        assert len(self.cardList) == len(holdCardList)
        for i in xrange(len(holdCardList)):
            if( self.cardList[i].num == Counter( self._countNumFromHands() ).most_common(1)[0][0] ):
                holdCardList[i] = True

        if( holdCardList == [False,False,False,False,False] ):
            return False
        return holdCardList

    def _holdHandFromTwoPare(self):
        holdCardList = [False,False,False,False,False]
        assert len(self.cardList) == len(holdCardList)
        for i in xrange(len(holdCardList)):
            if( self.cardList[i].num == Counter( self._countNumFromHands() ).most_common(1)[0][0] ):
                holdCardList[i] = True
            if( self.cardList[i].num == Counter( self._countNumFromHands() ).most_common(2)[1][0] ):
                holdCardList[i] = True

        if( holdCardList == [False,False,False,False,False] ):
            return False
        return holdCardList

    def _holdHandFromStraight(self,keepNum):
        #keepNumはハンドを残す枚数
        #ストレートにリーチなら4枚残すので、keepNum=4
        minStraightCardNum = 0
        holdCardList = [False,False,False,False,False]
        countStraightCard13_1 = self._countFromStraightList([10,11,12,13,1])
        for x in [1,2,3,4,5,6,7,8,9]:
            countStraightCard = self._countFromStraightList(range(x,x+5))
            if( countStraightCard >= keepNum):
                minStraightCardNum = x
        else:
            countStraightCard = self._countFromStraightList(range(minStraightCardNum,minStraightCardNum+5))

        if( countStraightCard >= keepNum or countStraightCard13_1 >=keepNum):
            #2枚くっつきを優先
            for x in range(2,minStraightCardNum+1):
                if( self._isExistNum(x) and self._isExistNum(x+1) ):
                    minStraightCardNum = x
            #リャンメン系を優先
            for x in range(2,minStraightCardNum+1):
                countLinkNum = 0
                for i in xrange(keepNum):
                    if( self._isExistNum(x+i) and self._isExistNum(x+i+1) ):
                        countLinkNum+=1
                if( countLinkNum == keepNum-1 ):
                    minStraightCardNum = x

        if( countStraightCard13_1 >= keepNum ):
            if( self._isExistJoker() ):
                holdCardList[self._posExistJoker()] = True

            overLapList = []
            for i in xrange(len(self.cardList)):
                for j in [10,11,12,13,1]:
                    if( (not self.cardList[i].num in overLapList) and\
                        self.cardList[i].num == j):
                        overLapList.append(j)
                        holdCardList[i] = True

            return holdCardList
        elif( countStraightCard >= keepNum ):
            if( self._isExistJoker() ):
                holdCardList[self._posExistJoker()] = True

            overLapList = []
            assert len(self.cardList) == len(holdCardList)
            for i in xrange(len(self.cardList)):
                for j in range(minStraightCardNum,minStraightCardNum+5):
                    if( (not self.cardList[i].num in overLapList) and\
                        self.cardList[i].num == j):
                        overLapList.append(j)
                        holdCardList[i] = True

            return holdCardList

        return False

    def _holdHandFromFlash(self,keepNum):
        #keepNumはハンドを残す枚数
        #フラッシュにリーチなら4枚残すので、keepNum=4
        holdCardList = [False,False,False,False,False]
        countSuit = self._countSuitFromHands()
        maxCountSuitKey = max(countSuit.items(), key=lambda x:x[1])[0]
        if(self._isExistJoker()):
            holdCardList[self._posExistJoker()] = True

            if( countSuit[maxCountSuitKey] >= keepNum-1 ):
                for i in xrange(len(self.cardList)):
                    if( maxCountSuitKey == self.cardList[i].suit ):
                        holdCardList[i] = True

                return(holdCardList)
        else:
            if( countSuit[maxCountSuitKey] == keepNum ):
                for i in xrange(len(self.cardList)):
                    if( maxCountSuitKey == self.cardList[i].suit ):
                        holdCardList[i] = True

                return(holdCardList)

        return False

    def _holdHandFromStraightFlash(self,keepNum):
        #keepNumはハンドを残す枚数
        #ストフラにリーチなら4枚残すので、keepNum=4
        if(not self._holdHandFromStraight(keepNum)):
            return False

        holdCardList = self._holdHandFromStraight(keepNum)

        countSuit = self._countSuitFromHands()
        maxCountSuit =  Counter(countSuit).most_common(1)[0][0]
        for i in xrange(len(holdCardList)):
            if( holdCardList[i] and \
              ( not self._isPosJoker(i) ) and\
              ( self.cardList[i].suit != maxCountSuit )):
                return False

        return holdCardList

    def judgeHand(self):
        #手役判定
        holdCardList = [False,False,False,False,False]

        #1 ロイヤルストレートフラッシュ
        if( (self._countFromStraightList([10,11,12,13,1])==5) and self._holdHandFromFlash(5) ):
            return(1,(True,True,True,True,True))

        #2 ファイブカード
        if( self._isExistJoker() and Counter(self._countNumFromHands()).most_common(1)[0][1] == 4):
            return(2,(True,True,True,True,True))

        #3 ストレートフラッシュ
        if( self._holdHandFromStraightFlash(5) ):
            return(3,(True,True,True,True,True))

        #4 フォーカード
        if( self._isExistJoker() ):
            if( Counter( self._countNumFromHands() ).most_common(1)[0][1] == 3):
                holdCardList = self._holdHandFromPare()
                holdCardList[self._posExistJoker()] = True
                return(4, holdCardList)
        else:
            if( Counter( self._countNumFromHands() ).most_common(1)[0][1] == 4):
                return(4, self._holdHandFromPare())

        #5 フルハウス
        pareDict = Counter( self._countNumFromHands() ).most_common(2)
        pareList = [pareDict[0][1],pareDict[1][1]]
        if( self._isExistJoker() ):
            if( pareList[0]==3 ):
                return(5, [True,True,True,True,True])
            elif( pareList[0]==2 and pareList[1]==2):
                return(5, [True,True,True,True,True])
        else:
            if( pareList[0]==3 and pareList[1]==2):
                return(5, [True,True,True,True,True])

        #6 ロイヤル 4枚残し
        if( (self._countFromStraightList([10,11,12,13,1])==4) and self._holdHandFromStraightFlash(4)):
            return(6,self._holdHandFromStraightFlash(4))

        #7 フラッシュ
        if( self._holdHandFromFlash(5) ):
            return(7,(True,True,True,True,True))

        #8 ストレート
        if( self._holdHandFromStraight(5) ):
            return(8,(True,True,True,True,True))

        #9 3カード
        if( self._isExistJoker() ):
            if( Counter( self._countNumFromHands() ).most_common(1)[0][1] == 2):
                holdCardList = self._holdHandFromPare()
                holdCardList[self._posExistJoker()] = True
                return(9, holdCardList)
        else:
            if( Counter( self._countNumFromHands() ).most_common(1)[0][1] == 3):
                return(9, self._holdHandFromPare())



        #10 2ペア
        if( not self._isExistJoker() ):
            pareDict = Counter( self._countNumFromHands() ).most_common(2)
            pareList = [pareDict[0][1],pareDict[1][1]]
            if( pareList[0]==2 and pareList[1]==2):
                return(10, self._holdHandFromTwoPare())

        #11 ストレートフラッシュ4枚残し
        if( self._holdHandFromStraightFlash(4) ):
            return(11, self._holdHandFromStraightFlash(4))

        #12 ロイヤル3枚残し
        if( (self._countFromStraightList([10,11,12,13,1])==3) and self._holdHandFromStraightFlash(3) ):
            return(12,self._holdHandFromStraightFlash(3))

        #13 ストレート4枚残し
        if( self._holdHandFromStraight(4) ):
            return(13,self._holdHandFromStraight(4))

        #14 1ペア
        if(self._isExistJoker()):
            holdCardList[self._posExistJoker()] = True
            return(14, holdCardList)
        else:
            if( Counter( self._countNumFromHands() ).most_common(1)[0][1] == 2):
                return(14, self._holdHandFromPare())

        #15 ストフラ3枚残し
        if( self._holdHandFromStraightFlash(3) ):
            return(15,self._holdHandFromStraightFlash(3))

        #16 ロイヤル2枚残し
        if( (self._countFromStraightList([10,11,12,13,1])==2) and self._holdHandFromStraightFlash(2)):
            return(16,self._holdHandFromStraightFlash(2))

        #17 ストレート3枚残し
        if( self._holdHandFromStraight(3) ):
            return(17,self._holdHandFromStraight(3))

        #18 フラッシュ4枚残し
        if( self._holdHandFromFlash(4)):
            return(18,self._holdHandFromFlash(4))

        ##これより下は確率的に狙いたくない
        #19 ストフラ2枚残し
        #20 ストレート2枚残し
        #21 フラッシュ3枚残し

        #0 全チェンジ
        return(0,(False,False,False,False,False))

class Game():
    def __init__(self,hands,status=0):
        self.hands = hands
        self.library = hands.showCards()
        self.status  = status

    def newCards(self,card1,card2):
        newcard = [A for A in card2 if not card1.isExist(A) ]
        return newcard

    def changeHands(self,cards):
        newcards=self.newCards(self.hands,cards)
        self.library.extend(newcards)
        self.cards=cards
        return self.cards,newcards

    def showLibrary(self):
        return self.library

if __name__ == '__main__':
    cards = Card()
    cards = [Card().setCard(u'h', 1), \
            Card().setCard(u's', 4), \
            Card().setCard(u'a', 5), \
            Card().setCard(u'd', 6), \
            Card().setCard(u's', 9)]
    hands = Hands()
    hands.setHands(cards)
    print hands.showCards()
    print hands.showHoldHandPos(1)
    print hands.showHandKeepingReason(0)