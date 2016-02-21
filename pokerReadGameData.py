# -*- coding: utf-8 -*-
import pokerHandsClass
import operation
import pokerDoubleUp

def handName(hand_id):
    if( hand_id == 11 ):
        return u'役なし'
    elif( hand_id == 10 ):
        return u'ワンペア'
    elif( hand_id == 9 ):
        return u'ツーペア'
    elif( hand_id == 8 ):
        return u'３カード'
    elif( hand_id == 7 ):
        return u'ストレート'
    elif( hand_id == 6 ):
        return u'フラッシュ'
    elif( hand_id == 5 ):
        return u'フルハウス'
    elif( hand_id == 4 ):
        return u'４カード'
    elif( hand_id == 3 ):
        return u'ストレートフラッシュ'
    elif( hand_id == 2 ):
        return u'５カード'
    elif( hand_id == 1 ):
        return u'ロイヤルストレートフラッシュ'

def readGameData(gameData):
    if( gameData.has_key(u'mbp_limit_info') ):
        print u"MyPage Loading"

    elif( gameData.has_key(u'data') ):
        if( gameData.has_key(u'option') ):
            print u"MsgData Loading"
        elif( gameData.get(u'data').has_key(u'se001') ):
            print u"mp3Data Loading"
        else:
            print u"anyData Loading"

    elif( gameData.has_key(u'other_game_play_flag') ):
        print u"Check playing other games"

    elif( gameData.get(u'reason')==0 and gameData.get(u'result')==True ):
        print u"Welcome Jewel Resort Casino"

    elif( gameData.get(u'hand_list')==[] ):
        print u"Poker Start"
        if( gameData.has_key(u'card_list') ):
            cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
            hands = pokerHandsClass.Hands(cards)
            print u"DealtHands:",
            print hands.showCards()
            print u"Hold:",
            print hands.showHoldHandPos(1)
            print u"Reason:",
            print hands.showHandKeepingReason(0)

            operation.sleepPlusRandom(3000)
            operation.clickHoldCard(hands.showHoldHandPos(0))
            operation.clickOK()

    elif( gameData.has_key(u'game_flag') ):
        print u"Restart Game"
        if( gameData.has_key(u'hand_list') ):
            print u"+ダブルアップ挑戦中+"
            card1 = _cardStrToCardClass(gameData[u'hand_list'].get(u'open_card'))
            payMedal = int(gameData.get(u'pay_medal'))
            remRound = 11-int(gameData.get(u'turn'))
            doubleup = pokerDoubleUp.DoubleUp(card1,False,payMedal,remRound)

            if( doubleup.judgeHiLow()==u'High' ):
                print u"High"
                operation.sleepPlusRandom(2000)
                operation.clickHigh()
            elif( doubleup.judgeHiLow()==u'Low' ):
                print u"Low"
                operation.sleepPlusRandom(2000)
                operation.clickLow()

    elif( gameData.has_key(u'card_list') and gameData.has_key(u'result') ):
        if( gameData.get(u'result')==u'win' ):
            cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
            hands = pokerHandsClass.Hands(cards)
            print u"ResultHands:",
            print hands.showCards()
            print u"Result:",
            print handName(gameData.get(u'hand_id'))

            print u"ダブルアップに挑戦しますか？ YES!"
            operation.sleepPlusRandom(2500)
            operation.clickYes()

        elif( gameData.get(u'result')==u'lose' ):
            if( gameData.has_key(u'hand') ):
                cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
                hands = pokerHandsClass.Hands(cards)
                print u"ResultHands:",
                print hands.showCards()
                print u"Result:",
                print handName(gameData.get(u'hand_id'))
                operation.sleepPlusRandom(2500)
                operation.clickStart()

    elif( gameData.has_key(u'next_game_flag') ):
        if( gameData.get(u'next_game_flag') ):
            if( gameData.get(u'result')==u'win' or gameData.get(u'result')==u'draw'):
                print gameData.get(u'result')
                print u"続行しますか？ NextCard = ",
                card1 = _cardStrToCardClass(gameData.get(u'card_first'))
                card2 = _cardStrToCardClass(gameData.get(u'card_second'))
                payMedal = int(gameData.get(u'pay_medal'))
                remRound = 11-int(gameData.get(u'turn'))
                doubleup = pokerDoubleUp.DoubleUp(card1,card2,payMedal,remRound)
                print doubleup.card2.num
                if( doubleup.isNextDoubleUp() ):
                    print u"YES"
                    operation.sleepPlusRandom(1500)
                    operation.clickYes()
                else:
                    print u"NO"
                    operation.sleepPlusRandom(1500)
                    operation.clickNo()

            elif( gameData.get(u'result')==u'lose' ):
                print u"lose"
                operation.sleepPlusRandom(1500)
                operation.clickStart()

        elif(not gameData.get(u'next_game_flag')):
            if( gameData.get(u'result')==u'win' ):
                print u"win"
                print u"ダブルアップ上限"
                operation.sleepPlusRandom(2000)
                operation.clickStart()
            elif( gameData.get(u'result')==u'draw' ):
                #10ラウンド目のダブルアップに引き分けた
                print u"draw"
                operation.sleepPlusRandom(2000)
                operation.clickStart()
            elif( gameData.get(u'result')==u'lose' ):
                #10ラウンド目のダブルアップに負けた
                print u"lose"
                operation.sleepPlusRandom(2000)
                operation.clickStart()

    elif( gameData.has_key(u'card_first') ):
        print u"+ダブルアップ挑戦中+"
        card1 = _cardStrToCardClass(gameData.get(u'card_first'))
        payMedal = int(gameData.get(u'pay_medal'))
        doubleup = pokerDoubleUp.DoubleUp(card1,False,payMedal,False)

        if( doubleup.judgeHiLow()==u'High' ):
            print u"High"
            operation.sleepPlusRandom(1500)
            operation.clickHigh()
        elif( doubleup.judgeHiLow()==u'Low' ):
            print u"Low"
            operation.sleepPlusRandom(1500)
            operation.clickLow()

    elif( gameData.has_key(u'card_list') ):
        cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
        hands = pokerHandsClass.Hands(cards)
        print u"DealtHands:",
        print hands.showCards()
        print u"Hold:",
        print hands.showHoldHandPos(1)
        print u"Reason:",
        print hands.showHandKeepingReason(0)

        operation.sleepPlusRandom(2000)
        operation.clickHoldCard(hands.showHoldHandPos(0))
        operation.clickOK()

    elif( gameData.has_key(u'status') ):
        getMedal = gameData[u'status'].get(u'get_medal')
        if( getMedal > 0):
            print u"get medal!!!"
            operation.sleepPlusRandom(2000)
            operation.clickStart()
        else:
            print u"Error: 知らないパターン003"
            print gameData

    elif( gameData.get(u'errorPopFlag') ):
        print u"Erorr: errorPopFlag=True"
        print gameData

    else:
        print u"Error: 知らないパターン999"
        print gameData

def _cardStrToCardClass(cardStr):
    cardInfo = cardStr.split(u"_")
    suit = False
    num = int(cardInfo[1])
    if( cardInfo[0] == u'1' ):
        suit = u's'
    elif( cardInfo[0] == u'2' ):
        suit = u'h'
    elif( cardInfo[0] == u'3' ):
        suit = u'd'
    elif( cardInfo[0] == u'4' ):
        suit = u'c'
    elif( cardInfo[0] == u'99' ):
        suit = u'99'
    else:
        return False

    newCard = pokerHandsClass.Card(suit,num)
    return newCard.getCard()

def _cardStrDictToCardClassList(cardDict):
    cards = [_cardStrToCardClass(cardDict.get(u'1')),
             _cardStrToCardClass(cardDict.get(u'2')),
             _cardStrToCardClass(cardDict.get(u'3')),
             _cardStrToCardClass(cardDict.get(u'4')),
             _cardStrToCardClass(cardDict.get(u'5'))]
    return cards

if __name__ == '__main__':
    '''
    cards = [('h', 8), \
            ('s', 11), \
            ('h', 12), \
            ('s', 9), \
            ('d', 6)]

    #print cards[1].suit, cards[1].num
    print cards
    hands = pokerHandsClass.Hands(cards)
    print hands.showCards()
    print hands.showHoldHandPos(1)
    operation.clickcard(hands.showHoldHandPos(1))
    operation.clickcenter()
    print hands.showHandKeepingReason(0)
    '''
