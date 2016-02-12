# -*- coding: utf-8 -*-
from collections import Counter

def countSuitFromHands(hands):
    ## ハンドにそのスートがいくつ含まれているか
    ### example
    # countList['s':1,'d':1,'c':2,'99':1]
    countDict = {}
    for i in hands:
        if( countDict.has_key(hands[i].suit) ):
            countDict[hands[i].suit] +=1
        else:
            countDict[hands[i].suit] = 1
    return countDict

def countNumFromHands(hands):
    ## ハンドにその数字がいくつ含まれているか
    ### example
    # countList[12:1,2:1,3:2,99:1]
    countDict = {}
    for i in hands:
        if( countDict.has_key(hands[i].num) ):
            countDict[hands[i].num] +=1
        else:
            countDict[hands[i].num] = 1
    return countDict

def isExistJoker(hands):
    for i in hands:
        if (hands[i].suit=='99' or hands[i].num == 99):
            return True
    else:
        return False

def posExistJoker(hands):
    for i in hands:
        if (hands[i].suit=='99' or hands[i].num == 99):
            return i
    else:
        return False

def isPosJoker(hands,i):
    #iにjokerはいるか
    if( hands[i].suit =='99' or hands[i].num == 99):
        return True
    return False

def isExistSuit(hands,suit):
    for i in hands:
        if (hands[i].suit==suit):
            return True
    else:
        return False

def isExistNum(hands,num):
    for i in hands:
        if (hands[i].num ==num):
            return True
    else:
        return False


def countFromStraightList(hands,straitList):
    #ハンドにリストの中のカードが何枚あるか
    countStraightCard = 0
    if( isExistJoker(hands) ):
        countStraightCard+=1

    overLapList = []
    for i in hands:
        for j in straitList:
            if( (not hands[i].num in overLapList) and\
              hands[i].num == j):
                overLapList.append(j)
                countStraightCard+=1
    return countStraightCard

def holdHandFromPare(hands):
    holdCardList = [False,False,False,False,False]
    for i in xrange(len(holdCardList)):
        if( hands[i].num == Counter( countNumFromHands(hands) ).most_common(1)[0][0] ):
            holdCardList[i] = True

    if( holdCardList == [False,False,False,False,False] ):
        return False
    return holdCardList

def holdHandFromStraight(hands,keepNum):
    #keepNumはハンドを残す枚数
    #ストレートにリーチなら4枚残すので、keepNum=4
    minStraightCardNum = 0
    holdCardList = [False,False,False,False,False]
    countStraightCard13_1 = countFromStraightList(hands, [10,11,12,13,1])
    for x in [1,2,3,4,5,6,7,8,9]:
        countStraightCard = countFromStraightList(hands, range(x,x+5))
        if( countStraightCard >= keepNum):
            minStraightCardNum = x
    else:
        countStraightCard = countFromStraightList(hands,range(minStraightCardNum,minStraightCardNum+5))

    #print countStraightCard
    if( countStraightCard >= keepNum or countStraightCard13_1 >=keepNum):
        #リャンメン系を優先
        for x in [2,3,4,5,6,7,8,9,10,11]:
            countLinkNum = 0
            for i in xrange(keepNum):
                if( isExistNum(hands, x+i) ):
                    countLinkNum+=1
            if( countLinkNum == keepNum ):
                minStraightCardNum = x

    if( countStraightCard13_1 >= keepNum ):
        if( posExistJoker(hands) ):
            holdCardList[posExistJoker(hands)] = True

        overLapList = []
        for i in hands:
            for j in [10,11,12,13,1]:
                if( (not hands[i].num in overLapList) and\
                    hands[i].num == j):
                    overLapList.append(j)
                    holdCardList[i] = True

        return holdCardList
    elif( countStraightCard >= keepNum ):
        if( posExistJoker(hands) ):
            holdCardList[posExistJoker(hands)] = True

        overLapList = []
        for i in hands:
            for j in range(minStraightCardNum,minStraightCardNum+5):
                if( (not hands[i].num in overLapList) and\
                    hands[i].num == j):
                    overLapList.append(j)
                    holdCardList[i] = True

        return holdCardList

    return False

def holdHandFromFlash(hands,keepNum):
    #keepNumはハンドを残す枚数
    #フラッシュにリーチなら4枚残すので、keepNum=4
    holdCardList = [False,False,False,False,False]
    countSuit = countSuitFromHands(hands)
    maxCountSuitKey = max(countSuit.items(), key=lambda x:x[1])[0]

    if(isExistJoker(hands)):
        if( posExistJoker(hands) ):
            holdCardList[posExistJoker(hands)] = True
        if( countSuit[maxCountSuitKey] >= keepNum-1 ):
            for i in hands:
                if( maxCountSuitKey == hands[i].suit ):
                    holdCardList[i] = True

            return(holdCardList)
    else:
        if( countSuit[maxCountSuitKey] == keepNum ):
            for i in hands:
                if( max(countSuit)==hands[i].suit ):
                    holdCardList[i] = True

            return(holdCardList)

    return False

def holdHandFromStraightFlash(hands,keepNum):
    #keepNumはハンドを残す枚数
    #ストフラにリーチなら4枚残すので、keepNum=4
    if(not holdHandFromStraight(hands, keepNum)):
        return False

    holdCardList = holdHandFromStraight(hands, keepNum)

    countSuit = countSuitFromHands(hands)
    maxCountSuit =  Counter(countSuit).most_common(1)[0][0]
    for i in xrange(len(holdCardList)):
        if( holdCardList[i] and \
          ( not isPosJoker(hands, i) ) and\
          ( hands[i].suit != maxCountSuit )):
            return False

    return holdCardList

def judgeHand(hands):
    #手役判定
    holdCardList = [False,False,False,False,False]

    #1 ロイヤルストレートフラッシュ
    if( (countFromStraightList(hands, [10,11,12,13,1])==5) and holdHandFromFlash(hands, 5) ):
        return(1,(True,True,True,True,True))

    #2 ファイブカード
    if( isExistJoker(hands) and Counter(countNumFromHands(hands)).most_common(1)[0][1] == 4):
        return(2,(True,True,True,True,True))

    #3 ストレートフラッシュ
    if( holdHandFromStraightFlash(hands, 5) ):
        return(3,(True,True,True,True,True))

    #4 フォーカード
    if( isExistJoker(hands) ):
        if( Counter( countNumFromHands(hands) ).most_common(1)[0][1] == 3):
            holdCardList = holdHandFromPare(hands)
            holdCardList[posExistJoker(hands)] = True
            return(4, holdCardList)
    else:
        if( Counter( countNumFromHands(hands) ).most_common(1)[0][1] == 4):
            return(4, holdHandFromPare(hands))

    #5 フルハウス
    pareDict = Counter( countNumFromHands(hands) ).most_common(2)
    pareList = [pareDict[0][1],pareDict[1][1]]
    if( isExistJoker(hands )):
        if( pareList[0]==3 ):
            holdCardList = holdHandFromPare(hands)
            holdHandFromPare(hands)[posExistJoker(hands)] = True
            return(5, holdCardList)
        elif( pareList[0]==2 and pareList[1]==2):
            holdCardList = holdHandFromPare(hands)
            holdHandFromPare(hands)[posExistJoker(hands)] = True
            return(5, holdCardList)
    else:
        if( pareList[0]==3 and pareList[1]==2):
            return(5, holdHandFromPare(hands))

    #6 ロイヤル 4枚残し
    if( (countFromStraightList(hands, [10,11,12,13,1])==4) and holdHandFromStraightFlash(hands, 4)):
        return(6,holdHandFromStraightFlash(hands, 4))

    #7 フラッシュ
    if( holdHandFromFlash(hands, 5) ):
        return(7,(True,True,True,True,True))

    #8 3カード
    if( isExistJoker(hands) ):
        if( Counter( countNumFromHands(hands) ).most_common(1)[0][1] == 2):
            holdCardList = holdHandFromPare(hands)
            holdCardList[posExistJoker(hands)] = True
            return(8, holdCardList)
    else:
        if( Counter( countNumFromHands(hands) ).most_common(1)[0][1] == 3):
            return(8, holdHandFromPare(hands))

    #9 ストレート
    if( holdHandFromStraight(hands, 5)):
        return(9,(True,True,True,True,True))

    #10 2ペア
    if( not isExistJoker(hands) ):
        pareDict = Counter( countNumFromHands(hands) ).most_common(2)
        pareList = [pareDict[0][1],pareDict[1][1]]
        if( pareList[0]==2 and pareList[1]==2):
            return(10, holdHandFromPare(hands))

    #11 ストレートフラッシュ4枚残し
    if( holdHandFromStraightFlash(hands, 4) ):
        return(11, holdHandFromStraightFlash(hands, 4))

    #12 ロイヤル3枚残し
    if( (countFromStraightList(hands, [10,11,12,13,1])==3) and holdHandFromStraightFlash(hands, 3)):
        return(12,holdHandFromStraightFlash(hands, 3))

    #13 ストレート4枚残し
    if( holdHandFromStraight(hands, 4) ):
        return(13,holdHandFromStraight(hands, 4))

    #14 1ペア
    if(isExistJoker(hands)):
        holdCardList[posExistJoker(hands)] = True
        return(14, holdCardList)
    else:
        if( Counter( countNumFromHands(hands) ).most_common(1)[0][1] == 2):
            return(14, holdHandFromPare(hands))

    #15 ストフラ3枚残し
    if( holdHandFromStraightFlash(hands, 3) ):
        return(15,holdHandFromStraightFlash(hands, 3))

    #16 ロイヤル2枚残し
    if( (countFromStraightList(hands, [10,11,12,13,1])==2) and holdHandFromStraightFlash(hands, 4)):
        return(16,holdHandFromStraightFlash(hands, 2))

    #17 ストレート3枚残し
    if( holdHandFromStraight(hands, 3) ):
        return(17,holdHandFromStraight(hands, 3))

    #18 フラッシュ4枚残し
    if( holdHandFromFlash(hands, 4)):
        return(18,holdHandFromFlash(hands, 4))

    ##これより下は確率的に狙いたくない
    #19 ストフラ2枚残し
    #20 ストレート2枚残し
    #21 フラッシュ3枚残し

    #0 全チェンジ
    return(0,(False,False,False,False,False))