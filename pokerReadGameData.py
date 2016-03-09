# -*- coding: utf-8 -*-
import pokerHandsClass
import pokerDoubleUp

def handName(hand_id):
    if( hand_id == 11 ):
        return u'役なし'
    elif( hand_id == 10 ):
        return u'ワンペア'
    elif( hand_id == 9 ):
        return u'ツーペア'
    elif( hand_id == 8 ):
        return u'スリーカード'
    elif( hand_id == 7 ):
        return u'ストレート'
    elif( hand_id == 6 ):
        return u'フラッシュ'
    elif( hand_id == 5 ):
        return u'フルハウス'
    elif( hand_id == 4 ):
        return u'フォーカード'
    elif( hand_id == 3 ):
        return u'ストレートフラッシュ'
    elif( hand_id == 2 ):
        return u'ファイブカード'
    elif( hand_id == 1 ):
        return u'ロイヤルストレートフラッシュ'
    else:
        return False

def readGameData(gameData):
    if( gameData.has_key(u'errorPopFlag') ):
        if( gameData.get(u'errorPopFlag')==True):
            print u"Erorr: errorPopFlag=True"
            print gameData
            return {u'status':u'ERROR_POP_FLAG_TRUE',u'data':gameData}

    if( gameData.has_key(u'mbp_limit_info') ):
        print u"MyPage Loading"
        return {u'status':u'MYPAGE_LOADING'}

    elif( gameData.has_key(u'data') ):
        if( gameData.has_key(u'option') ):
            print u"MsgData Loading"
            return {u'status':u'MSGDATA_LOADING'}
        elif( gameData.get(u'data').has_key(u'se001') ):
            print u"mp3Data Loading"
            return {u'status':u'MP3DATA_LOADING'}
        else:
            print u"anyData Loading"
            return {u'status':u'ANYDATA_LOADING'}

    elif( gameData.has_key(u'other_game_play_flag') ):
        print u"Check playing other games"
        return {u'status':u'CHECK_PLAYING_OTHER_GAMES'}

    elif( gameData.get(u'reason')==0 and gameData.get(u'result')==True ):
        print u"Welcome Jewel Resort Casino"
        return {u'status':u'WELCOME_CASINO'}

    elif( gameData.get(u'game_flag')==u'0' or gameData.get(u'game_flag')==0):
        print u"Poker Start"
        return {u'status':u'POKER_START'}

    elif( gameData.get(u'game_flag')==u'10'):
        cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
        hands = pokerHandsClass.Hands()
        hands.setHands(cards)
        print u"DealtHands:",
        print hands.showCards()
        print u"Hold:",
        print hands.showHoldHandPos(1)
        print u"Reason:",
        print hands.showHandKeepingReason(0)

        return {u'status':u'GAME_START',u'Hands':hands}

    elif( gameData.get(u'game_flag')==u'15'):
        cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
        hands = pokerHandsClass.Hands()
        hands.setHands(cards)
        print u"ResultHands:",
        print hands.showCards()
        print u"Result:",
        print handName(gameData.get(u'hand_id'))

        print u"ダブルアップに挑戦しますか？ YES!"

        return {u'status':u'RESTART_GAME_WIN',u'Hands':hands}

    elif( gameData.get(u'game_flag')==u'20'):
        if( gameData.has_key(u'hand_list') ):
            print u"+ダブルアップ挑戦中+"
            card1 = _cardStrToCardClass(gameData[u'hand_list'].get(u'open_card'))
            payMedal = int(gameData.get(u'pay_medal'))
            remRound = 11-int(gameData.get(u'turn'))
            doubleup = pokerDoubleUp.DoubleUp(card1,False,payMedal,remRound)

            if( doubleup.judgeHiLow()==u'High' ):
                print u"High"
                return {u'status':u'RESTART_DOUBLEUP_HIGH'}

            elif( doubleup.judgeHiLow()==u'Low' ):
                print u"Low"
                return {u'status':u'RESTART_DOUBLEUP_LOW'}

    elif( gameData.get(u'game_flag')==u'22'):
        print u"Restart Game"
        print u"続行しますか？ NextCard = ",
        card1 = _cardStrToCardClass(gameData.get(u'hand_list').get(u'open_card_old'))
        card2 = _cardStrToCardClass(gameData.get(u'hand_list').get(u'close_card_old'))
        payMedal = int(gameData.get(u'pay_medal'))
        remRound = 11-int(gameData.get(u'turn'))
        doubleup = pokerDoubleUp.DoubleUp(card1,card2,payMedal,remRound)
        print doubleup.card2.num
        if( doubleup.isNextDoubleUp() ):
            print u"YES"
            return {u'status':u'IS_NEXT_DOUBLEUP_YES',u'DoubleUp':doubleup}
        else:
            print u"NO"
            return {u'status':u'IS_NEXT_DOUBLEUP_NO',u'DoubleUp':doubleup}

    elif( gameData.has_key(u'card_list') and gameData.has_key(u'result') ):
        if( gameData.get(u'result')==u'win' ):
            cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
            hands = pokerHandsClass.Hands()
            hands.setHands(cards)
            print u"ResultHands:",
            print hands.showCards()
            print u"Result:",
            print handName(gameData.get(u'hand_id'))

            print u"ダブルアップに挑戦しますか？ YES!"

            return {u'status':u'GAME_WIN',u'Hands':hands,u'hand_name':handName(gameData.get(u'hand_id'))}

        elif( gameData.get(u'result')==u'lose' ):
            if( gameData.has_key(u'hand') ):
                cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
                hands = pokerHandsClass.Hands()
                hands.setHands(cards)
                print u"ResultHands:",
                print hands.showCards()
                print u"Result:",
                print handName(gameData.get(u'hand_id'))

                return {u'status':u'GAME_LOSE',u'Hands':hands,u'hand_name':handName(gameData.get(u'hand_id'))}

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
                    return {u'status':u'IS_NEXT_DOUBLEUP_YES',u'result':gameData.get(u'result'),u'DoubleUp':doubleup}
                else:
                    print u"NO"
                    return {u'status':u'IS_NEXT_DOUBLEUP_NO',u'result':gameData.get(u'result'),u'DoubleUp':doubleup}

            elif( gameData.get(u'result')==u'lose' ):
                print u"lose"
                return {u'status':u'DOUBLEUP_LOSE'}

        elif(not gameData.get(u'next_game_flag')):
            if( gameData.get(u'result')==u'win' and gameData.has_key(u'pay_medal') ):
                getMedal = gameData.get(u'pay_medal')
                haveMedal = gameData.get(u'medal').get(u'number')
                print u"win"
                print u"ダブルアップ上限"
                return {u'status':u'DOUBLEUP_MAX',u'get':getMedal,u'have_medal':haveMedal}

            elif( gameData.get(u'result')==u'draw' ):
                #10ラウンド目のダブルアップに引き分けた
                getMedal = gameData.get(u'pay_medal')
                haveMedal = gameData.get(u'medal').get(u'number')
                print u"draw"
                return {u'status':u'DOUBLEUP_10ROUND_DRAW',u'get':getMedal,u'have_medal':haveMedal}

            elif( gameData.get(u'result')==u'lose' ):
                #10ラウンド目のダブルアップに負けた
                print u"lose"
                return {u'status':u'DOUBLEUP_10ROUND_LOSE'}

    elif( gameData.has_key(u'card_first') ):
        print u"+ダブルアップ挑戦中+"
        card1 = _cardStrToCardClass(gameData.get(u'card_first'))
        payMedal = int(gameData.get(u'pay_medal'))
        doubleup = pokerDoubleUp.DoubleUp(card1,False,payMedal,False)

        if( doubleup.judgeHiLow()==u'High' ):
            print u"High"
            return {u'status':u'DOUBLEUP_HIGH'}

        elif( doubleup.judgeHiLow()==u'Low' ):
            print u"Low"
            return {u'status':u'DOUBLEUP_LOW'}

    elif( gameData.has_key(u'card_list') ):
        print gameData.get(u'card_list')
        cards = _cardStrDictToCardClassList(gameData.get(u'card_list'))
        hands = pokerHandsClass.Hands()
        hands.setHands(cards)
        print u"DealtHands:",
        print hands.showCards()
        print u"Hold:",
        print hands.showHoldHandPos(1)
        print u"Reason:",
        print hands.showHandKeepingReason(0)

        return {u'status':u'GAME_START',u'Hands':hands}

    elif( gameData.has_key(u'status') ):
        #print gameData[u'status']
        if( gameData[u'status'].has_key(u'get_medal') ):
            getMedal = gameData[u'status'].get(u'get_medal')
            haveMedal = gameData[u'status'].get(u'medal').get(u'number')
            if( getMedal > 0):
                print u"get medal!!!"
                return {u'status':u'GET_MEDAL',u'get':getMedal,u'have_medal':haveMedal}
            else:
                print u"Error: 知らないパターン003"
                print gameData

                return {u'status':u'UNKNOWN',u'data':gameData,u'num':003}
        else:
            print u"Error: 知らないパターン004"
            print gameData

            return {u'status':u'UNKNOWN',u'data':gameData,u'num':004}

    else:
        print u"Error: 知らないパターン999"
        print gameData

        return {u'status':u'UNKNOWN',u'data':gameData,u'num':999}

def _cardStrToCardClass(cardStr):
    cardInfo = cardStr.split(u"_")
    suit = ""
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

    newCard = pokerHandsClass.Card()
    newCard.setCard(suit, num)
    return newCard.getCard()

def _cardStrDictToCardClassList(cardDict):
    cards = [_cardStrToCardClass(cardDict.get(u'1')),
             _cardStrToCardClass(cardDict.get(u'2')),
             _cardStrToCardClass(cardDict.get(u'3')),
             _cardStrToCardClass(cardDict.get(u'4')),
             _cardStrToCardClass(cardDict.get(u'5'))]
    return cards

if __name__ == '__main__':
    pass