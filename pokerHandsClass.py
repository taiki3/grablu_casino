# -*- coding: utf-8 -*-
from collections import Counter

class Card:
    def __init__(self,suit,num):
        self.suit = suit
        self.num = num

    def showSuit(self):
        return self.suit

    def showNum(self):
        return self.num

    def setCard(self,suit,num):
        self.suit = suit
        self.num = num

    def compareCard(self,cardB):
        if self.num == cardB.num and self.suit == cardB.suit:
            return True
        else:
            return False

class Hands:
    def __init__(self,cards):
        assert type(cards) == list
        if( len(cards)== 5 ):
            self.cardList = cards
            self.handPattern = False
            self.holdPos = False
        else:
            return False

    def shoHoldHandPos(self,isRedoJudge):
        # isRedoJudge ジャッジ関数を呼び直す？
        # return list
        if(isRedoJudge):
            handPattern,holdPos = self.judgeHand()
            self.handPattern = handPattern
            self.holdPos = holdPos
            return self.holdPos
        elif(not self.holdPos):
            return False
        else:
            return self.holdPos

    def showHandKeepingReason(self,isRedoJudge):
        # isRedoJudge ジャッジ関数を呼び直す？
        # return str
        if(isRedoJudge):
            handPattern,holdPos = self.judgeHand()
            self.handPattern = handPattern
            self.holdPos = holdPos
        elif(not self.handPattern):
            return False
        else:
            pass

        if(handPattern==1):
            return  "+ロイヤルストレートフラッシュ+"
        elif(handPattern==2):
            return "+ファイブカード+"
        elif(handPattern==3):
            return "+ストレートフラッシュ+"
        elif(handPattern==4):
            return "+フォーカード+"
        elif(handPattern==5):
            return "+フルハウス+"
        elif(handPattern==6):
            return "+ロイヤル4枚残し+"
        elif(handPattern==7):
            return "+フラッシュ+"
        elif(handPattern==8):
            return "+ストレート+"
        elif(handPattern==9):
            return "+3カード+"
        elif(handPattern==10):
            return "+2ペア+"
        elif(handPattern==11):
            return "+ストレートフラッシュ4枚残し+"
        elif(handPattern==12):
            return "+ロイヤル3枚残し+"
        elif(handPattern==13):
            return "+ストレート4枚残し+"
        elif(handPattern==14):
            return "+1ペア+"
        elif(handPattern==15):
            return "+ストフラ3枚残し+"
        elif(handPattern==16):
            return "+ロイヤル2枚残し+"
        elif(handPattern==17):
            return "+ストレート3枚残し+"
        elif(handPattern==18):
            return "+フラッシュ4枚残し+"
        elif(handPattern==19):
            return "+ストフラ2枚残し+"
        elif(handPattern==20):
            return "+ストレート2枚残し+"
        elif(handPattern==21):
            return "+フラッシュ3枚残し+"
        else:
            return "+全チェンジ+"

    def showCards(self):
        return self.cardList

    def isExistCard(self,card):
        for v in self.cardList:
            if v.compareCard(card):
                return True
            else:
                return False

    def countSuitFromHands(self):
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

    def countNumFromHands(self):
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

    def isExistJoker(self):
        for card in self.cardList:
            if (card.suit=='99' or card.num == 99):
                return True
        else:
            return False

    def posExistJoker(self):
        for i in xrange(len(self.cardList)):
            if (self.cardList[i].suit=='99' or self.cardList[i].num == 99):
                return i
        else:
            return False

    def isPosJoker(self,pos):
        #iの位置にjokerはいるか
        if( self.cardList[pos].suit =='99' or self.cardList[pos].num == 99):
            return True
        return False

    def isExistSuit(self,suit):
        for card in self.cardList:
            if (card.suit==suit):
                return True
        else:
            return False

    def isExistNum(self,num):
        for card in self.cardList:
            if (card.num==num):
                return True
        else:
            return False

    def countFromStraightList(self,straitList):
        #ハンドにリストの中のカードが何枚あるか
        countStraightCard = 0
        if( self.isExistJoker() ):
            countStraightCard+=1

        overLapList = []
        for card in self.cardList:
            for j in straitList:
                if( (not card.num in overLapList) and\
                  card.num == j):
                    overLapList.append(j)
                    countStraightCard+=1
        return countStraightCard

    def holdHandFromPare(self):
        holdCardList = [False,False,False,False,False]
        assert len(self.cardList) == len(holdCardList)
        for i in xrange(len(holdCardList)):
            if( self.cardList[i].num == Counter( self.countNumFromHands() ).most_common(1)[0][0] ):
                holdCardList[i] = True

        if( holdCardList == [False,False,False,False,False] ):
            return False
        return holdCardList

    def holdHandFromStraight(self,keepNum):
        #keepNumはハンドを残す枚数
        #ストレートにリーチなら4枚残すので、keepNum=4
        minStraightCardNum = 0
        holdCardList = [False,False,False,False,False]
        countStraightCard13_1 = self.countFromStraightList([10,11,12,13,1])
        for x in [1,2,3,4,5,6,7,8,9]:
            countStraightCard = self.countFromStraightList(range(x,x+5))
            if( countStraightCard >= keepNum):
                minStraightCardNum = x
        else:
            countStraightCard = self.countFromStraightList(range(minStraightCardNum,minStraightCardNum+5))

        #print countStraightCard
        if( countStraightCard >= keepNum or countStraightCard13_1 >=keepNum):
            #リャンメン系を優先
            for x in [2,3,4,5,6,7,8,9,10,11]:
                countLinkNum = 0
                for i in xrange(keepNum):
                    if( self.isExistNum(x+i) ):
                        countLinkNum+=1
                if( countLinkNum == keepNum ):
                    minStraightCardNum = x

        if( countStraightCard13_1 >= keepNum ):
            if( self.posExistJoker() ):
                holdCardList[self.posExistJoker()] = True

            overLapList = []
            for i in xrange(len(self.cardList)):
                for j in [10,11,12,13,1]:
                    if( (not self.cardList[i].num in overLapList) and\
                        self.cardList[i].num == j):
                        overLapList.append(j)
                        holdCardList[i] = True

            return holdCardList
        elif( countStraightCard >= keepNum ):
            if( self.posExistJoker() ):
                holdCardList[self.posExistJoker()] = True

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

    def holdHandFromFlash(self,keepNum):
        #keepNumはハンドを残す枚数
        #フラッシュにリーチなら4枚残すので、keepNum=4
        holdCardList = [False,False,False,False,False]
        countSuit = self.countSuitFromHands()
        maxCountSuitKey = max(countSuit.items(), key=lambda x:x[1])[0]

        if(self.isExistJoker()):
            if( self.posExistJoker() ):
                holdCardList[self.posExistJoker()] = True
            if( countSuit[maxCountSuitKey] >= keepNum-1 ):
                for i in xrange(len(self.cardList)):
                    if( maxCountSuitKey == self.cardList[i].suit ):
                        holdCardList[i] = True

                return(holdCardList)
        else:
            if( countSuit[maxCountSuitKey] == keepNum ):
                for i in xrange(len(self.cardList)):
                    if( max(countSuit)==self.cardList[i].suit ):
                        holdCardList[i] = True

                return(holdCardList)

        return False

    def holdHandFromStraightFlash(self,keepNum):
        #keepNumはハンドを残す枚数
        #ストフラにリーチなら4枚残すので、keepNum=4
        if(not self.holdHandFromStraight(keepNum)):
            return False

        holdCardList = self.holdHandFromStraight(keepNum)

        countSuit = self.countSuitFromHands()
        maxCountSuit =  Counter(countSuit).most_common(1)[0][0]
        for i in xrange(len(holdCardList)):
            if( holdCardList[i] and \
              ( not self.isPosJoker(i) ) and\
              ( self.cardList[i].suit != maxCountSuit )):
                return False

        return holdCardList

    def judgeHand(self):
        #手役判定
        holdCardList = [False,False,False,False,False]

        #1 ロイヤルストレートフラッシュ
        if( (self.countFromStraightList([10,11,12,13,1])==5) and self.holdHandFromFlash(5) ):
            return(1,(True,True,True,True,True))

        #2 ファイブカード
        if( self.isExistJoker() and Counter(self.countNumFromHands()).most_common(1)[0][1] == 4):
            return(2,(True,True,True,True,True))

        #3 ストレートフラッシュ
        if( self.holdHandFromStraightFlash(5) ):
            return(3,(True,True,True,True,True))

        #4 フォーカード
        if( self.isExistJoker() ):
            if( Counter( self.countNumFromHands() ).most_common(1)[0][1] == 3):
                holdCardList = self.holdHandFromPare()
                holdCardList[self.posExistJoker()] = True
                return(4, holdCardList)
        else:
            if( Counter( self.countNumFromHands() ).most_common(1)[0][1] == 4):
                return(4, self.holdHandFromPare())

        #5 フルハウス
        pareDict = Counter( self.countNumFromHands() ).most_common(2)
        pareList = [pareDict[0][1],pareDict[1][1]]
        if( self.isExistJoker() ):
            if( pareList[0]==3 ):
                return(5, [True,True,True,True,True])
            elif( pareList[0]==2 and pareList[1]==2):
                return(5, [True,True,True,True,True])
        else:
            if( pareList[0]==3 and pareList[1]==2):
                return(5, [True,True,True,True,True])

        #6 ロイヤル 4枚残し
        if( (self.countFromStraightList([10,11,12,13,1])==4) and self.holdHandFromStraightFlash(4)):
            return(6,self.holdHandFromStraightFlash(4))

        #7 フラッシュ
        if( self.holdHandFromFlash(5) ):
            return(7,(True,True,True,True,True))

        #8 ストレート
        if( self.holdHandFromStraight(5) ):
            return(8,(True,True,True,True,True))

        #9 3カード
        if( self.isExistJoker() ):
            if( Counter( self.countNumFromHands() ).most_common(1)[0][1] == 2):
                holdCardList = self.holdHandFromPare()
                holdCardList[self.posExistJoker()] = True
                return(9, holdCardList)
        else:
            if( Counter( self.countNumFromHands() ).most_common(1)[0][1] == 3):
                return(9, self.holdHandFromPare())



        #10 2ペア
        if( not self.isExistJoker() ):
            pareDict = Counter( self.countNumFromHands() ).most_common(2)
            pareList = [pareDict[0][1],pareDict[1][1]]
            if( pareList[0]==2 and pareList[1]==2):
                return(10, self.holdHandFromPare())

        #11 ストレートフラッシュ4枚残し
        if( self.holdHandFromStraightFlash(4) ):
            return(11, self.holdHandFromStraightFlash(4))

        #12 ロイヤル3枚残し
        if( (self.countFromStraightList([10,11,12,13,1])==3) and self.holdHandFromStraightFlash(3) ):
            return(12,self.holdHandFromStraightFlash(3))

        #13 ストレート4枚残し
        if( self.holdHandFromStraight(4) ):
            return(13,self.holdHandFromStraight(4))

        #14 1ペア
        if(self.isExistJoker()):
            holdCardList[self.posExistJoker()] = True
            return(14, holdCardList)
        else:
            if( Counter( self.countNumFromHands() ).most_common(1)[0][1] == 2):
                return(14, self.holdHandFromPare())

        #15 ストフラ3枚残し
        if( self.holdHandFromStraightFlash(3) ):
            return(15,self.holdHandFromStraightFlash(3))

        #16 ロイヤル2枚残し
        if( (self.countFromStraightList([10,11,12,13,1])==2) and self.holdHandFromStraightFlash(2)):
            return(16,self.holdHandFromStraightFlash(2))

        #17 ストレート3枚残し
        if( self.holdHandFromStraight(3) ):
            return(17,self.holdHandFromStraight(3))

        #18 フラッシュ4枚残し
        if( self.holdHandFromFlash(4)):
            return(18,self.holdHandFromFlash(4))

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
    cards1 = [Card(i,1,v) for i,v in enumerate([1,13,4,2,8])]
    cards2 = [Card(i,1,u) for i,u in enumerate([1,13,4,5,9])]
    hands1 = Hands(cards1)
    game1 = Game(hands1)
    game1.changeHands(cards2)
    for v in game1.showLibrary():
        print(v.showSuit(),v.showNum())
