# -*- coding: utf-8 -*-
from collections import Counter
# 手役判定 ###
def judgeHand(hands):
    #for key,value in sorted(hands.items(),key=lambda x:x[1].num):
    #    print key,value.suit,value.num
    #for i in hands:
    #    print hands[i].suit, hands[i].num

    isJokerFlag = False
    isFlashFlag = False
    isStraightFlag = False

    sortedHands = sorted(hands.items(),key=lambda x:x[1].num)
    holdCardList = [False,False,False,False,False]

    # ジョーカー所持フラグ
    for i in hands:
        if( hands[i].suit == '99' or hands[i].num == 99):
            isJokerFlag = True
            break

    # フラッシュflag
    if(isJokerFlag):
        for i in hands:
            if( i >= len(hands) ):
                break
            if( hands[i].suit != hands[i+1].suit):
                if( hands[i].suit == '99' or hands[i+1].suit == '99' or \
                  hands[i].num == 99 or hands[i+1].num == 99):
                    isFlashFlag = True
                else:
                    isFlashFlag = False
                    break
            else:
                isFlashFlag = True
    elif( hands[1].suit == hands[2].suit == hands[3].suit == hands[4].suit == hands[5].suit ):
        isFlashFlag = True
    else:
        isFlashFlag = False

    # ストレートflag
    if(isJokerFlag):
        if( sortedHands[0][1].num == 1 ):
            ################
            # 10 11 12    A
            # 10 11    13 A
            # 10    12 13 A
            #    11 12 13 A
            ################
            if( sortedHands[1][1].num == 10 and sortedHands[2][1].num == 11 and sortedHands[3][1].num == 12):
                isStraightFlag = True
            elif( sortedHands[1][1].num == 10 and sortedHands[2][1].num == 11 and sortedHands[3][1].num == 13):
                isStraightFlag = True
            elif( sortedHands[1][1].num == 10 and sortedHands[2][1].num == 12 and sortedHands[3][1].num == 13):
                isStraightFlag = True
            elif( sortedHands[1][1].num == 11 and sortedHands[2][1].num == 12 and sortedHands[3][1].num == 13):
                isStraightFlag = True
            else:
                pass

        if( sortedHands[3][1].num-sortedHands[0][1].num < 5 ):
            ################
            # 1 2 3 4
            # 1 2 3   5
            # 1 2   4 5
            # 1   3 4 5
            #   2 3 4 5
            ################
            minValue = sortedHands[0][1].num
            if( sortedHands[1][1].num == minValue+1 and sortedHands[2][1].num == minValue+2 and sortedHands[3][1].num == minValue+3):
                isStraightFlag = True
            elif( sortedHands[1][1].num == minValue+1 and sortedHands[2][1].num == minValue+2 and sortedHands[3][1].num == minValue+4):
                isStraightFlag = True
            elif( sortedHands[1][1].num == minValue+1 and sortedHands[2][1].num == minValue+3 and sortedHands[3][1].num == minValue+4):
                isStraightFlag = True
            elif( sortedHands[1][1].num == minValue+2 and sortedHands[2][1].num == minValue+3 and sortedHands[3][1].num == minValue+4):
                isStraightFlag = True
            else:
                isStraightFlag = False

        else:
            if(not isStraightFlag): #Flagを上書きしない
                isStraightFlag = False

    elif( sortedHands[4][1].num-sortedHands[0][1].num < 5 ):
        if( sortedHands[0][1].num == 1 and sortedHands[1][1].num == 10 and \
           sortedHands[2][1].num == 11 and sortedHands[3][1].num == 12 and sortedHands[4][1].num == 13):
            isStraightFlag = True

        elif( sortedHands[0][1].num+1 == sortedHands[1][1].num and sortedHands[1][1].num+1 == sortedHands[2][1].num and \
           sortedHands[2][1].num+1 == sortedHands[3][1].num and sortedHands[3][1].num+1 == sortedHands[4][1].num ):
            isStraightFlag = True

        else:
            isStraightFlag = False
    else:
        isStraightFlag = False

    ## デバッグ用出力
    for i in hands:
        print hands[i].suit+str(hands[i].num),
    print ""

    for i in xrange(len(sortedHands)):
        print sortedHands[i][1].suit+str(sortedHands[i][1].num), #[1]とかいうおまじない
    print ""

    #1 ロイヤルストレートフラッシュ
    if(isFlashFlag and isStraightFlag):
        if(isJokerFlag):
            if( sortedHands[0][1].num == 1 ):
                if( sortedHands[1][1].num == 10 and sortedHands[2][1].num == 11 and sortedHands[3][1].num == 12):
                    return(1,(True,True,True,True,True))
                elif( sortedHands[1][1].num == 10 and sortedHands[2][1].num == 11 and sortedHands[3][1].num == 13):
                    return(1,(True,True,True,True,True))
                elif( sortedHands[1][1].num == 10 and sortedHands[2][1].num == 12 and sortedHands[3][1].num == 13):
                    return(1,(True,True,True,True,True))
                elif( sortedHands[1][1].num == 11 and sortedHands[2][1].num == 12 and sortedHands[3][1].num == 13):
                    return(1,(True,True,True,True,True))
                else:
                    pass

            if( sortedHands[0][1].num == 10 and sortedHands[1][1].num == 11 and \
               sortedHands[2][1].num == 12 and sortedHands[3][1].num == 13):
                    return(1,(True,True,True,True,True))
        else:
            if( sortedHands[0][1].num == 1 and sortedHands[1][1].num == 10 and \
               sortedHands[2][1].num == 11 and sortedHands[3][1].num == 12 and sortedHands[4][1].num == 13):
                return(1,(True,True,True,True,True))

    #2 ファイブカード
    if(isJokerFlag):
        valueCount = {}
        for i in hands:
            if( valueCount.has_key(hands[i].num) ):
                valueCount[hands[i].num] +=1
            else:
                valueCount[hands[i].num] = 1

        maxCountKey = max(valueCount.items(), key=lambda x:x[1])[0]
        if( valueCount[maxCountKey] == 4):
            return(2,(True,True,True,True,True))

    #3 ストレートフラッシュ
    if(isFlashFlag and isStraightFlag):
        return(3,(True,True,True,True,True))

    #4 フォーカード
    valueCount = {}
    for i in hands:
        if( valueCount.has_key(hands[i].num) ):
            valueCount[hands[i].num] +=1
        else:
            valueCount[hands[i].num] = 1

    maxCountKey = max(valueCount.items(), key=lambda x:x[1])[0]
    if(isJokerFlag):
        if( valueCount[maxCountKey] == 3 ):
            for i in hands:
                if( hands[i].num == 99 ):
                    holdCardList[i-1] = True
                elif( maxCountKey ==hands[i].num ):
                    holdCardList[i-1] = True

            return(4,holdCardList)
    else:
        if( valueCount[maxCountKey] == 4 ):
            for i in hands:
                if( max(valueCount)==hands[i].num ):
                    holdCardList[i-1] = True

            return(4,holdCardList)

    #5 フルハウス
    if(isJokerFlag):
        valueCount = {}
        for i in hands:
            if( valueCount.has_key(hands[i].num) ):
                valueCount[hands[i].num] +=1
            else:
                valueCount[hands[i].num] = 1

        maxCountkey = max(valueCount.items(), key=lambda x:x[1])[0]
        if( valueCount[maxCountkey]==3 ):
            return(5,(True,True,True,True,True))
        elif( valueCount[maxCountkey]==2 ):
            countTwoPareCard = 0
            for i in valueCount:
                if( valueCount[i] == 2 ):
                    countTwoPareCard+=1

            if( countTwoPareCard == 2):
                return(5,(True,True,True,True,True))
    else:
        valueCount = {}
        for i in hands:
            if( valueCount.has_key(hands[i].num) ):
                valueCount[hands[i].num] +=1
            else:
                valueCount[hands[i].num] = 1

        threePareKey = max(valueCount.items(), key=lambda x:x[1])[0]
        twoPareKey = min(valueCount.items(), key=lambda x:x[1])[0]
        if( valueCount[threePareKey] == 3 and valueCount[twoPareKey] == 2):
            return(5,(True,True,True,True,True))
    #6 ロイヤル 4枚残し
    countSuit = {}
    for i in hands:
        if( countSuit.has_key(hands[i].suit) ):
            countSuit[hands[i].suit] +=1
        else:
            countSuit[hands[i].suit] = 1

    maxCountSuitKey = max(countSuit.items(), key=lambda x:x[1])[0]
    maxCountSuit =  Counter(countSuit).most_common(1)[0][0]
    if( countSuit[maxCountSuitKey] >= 4 ):
        countRoyalStraightCard = 0
        for i in hands:
            if( hands[i].num == 99 or hands[i].suit == '99' ):
                countRoyalStraightCard+=1
            for j in [1,10,11,12,13]:
                if( hands[i].num == j and hands[i].suit == maxCountSuit ):
                    countRoyalStraightCard+=1

        if(countRoyalStraightCard >= 4):
            for i in hands:
                if( hands[i].num==99 or hands[i].suit==99):
                    holdCardList[i-1] = True
                for j in [1,10,11,12,13]:
                    if( hands[i].num == j and hands[i].suit == maxCountSuit ):
                        holdCardList[i-1] = True

            return(6,holdCardList)
    #7 フラッシュ
    #8 3カード
    #9 ストレート
    #10 2ペア
    #11 ストレートフラッシュ4枚残し
    #12 ロイヤル3枚残し
    #13 ストレート4枚残し
    #14 1ペア
    #15 ストフラ3枚残し
    #16 ロイヤル2枚残し
    #17 ストレート3枚残し
    #18 フラッシュ4枚残し
    #19 ストフラ2枚残し
    #20 ストレート2枚残し
    #21 フラッシュ3枚残し

    if(isJokerFlag):
        print "ジョーカー"
    if(isStraightFlag):
        print "ストレート"
    if(isFlashFlag):
        print "フラッシュ"

    return(-1,(False,False,False,False,False))