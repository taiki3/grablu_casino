# -*- coding: utf-8 -*-
import xmlpac as xpc
import pokerHandsClass
import operation
import pokerDoubleUp
from win32api import Sleep

def handName(hand_id):
    if( hand_id == 11 ):
        return '役なし'
    elif( hand_id == 10 ):
        return 'ワンペア'
    elif( hand_id == 9 ):
        return 'ツーペア'
    elif( hand_id == 8 ):
        return '３カード'
    elif( hand_id == 7 ):
        return 'ストレート'
    elif( hand_id == 6 ):
        return 'フラッシュ'
    elif( hand_id == 5 ):
        return 'フルハウス'
    elif( hand_id == 4 ):
        return '４カード'
    elif( hand_id == 3 ):
        return 'ストレートフラッシュ'
    elif( hand_id == 2 ):
        return '５カード'
    elif( hand_id == 1 ):
        return 'ロイヤルストレートフラッシュ'

def readPacket(packet):
    if( packet.has_key('card_list') and packet.has_key('result') ):
        if( packet.get('result')=='win' ):
            print "ダブルアップに挑戦しますか？ YES!"
            #YESをクリック
            Sleep(2500)
            operation.clickright()
        elif( packet.get('result')=='lose' ):
            if( packet.has_key('hand') ):
                cards = xpc.listToCardClassList(packet,'card_list')
                hands = pokerHandsClass.Hands(cards)
                print "ResultHands:",
                print hands.showCards()
                print "Result:",
                print handName(packet.get('hand_id'))
                #STARTをクリック
                Sleep(2500)
                operation.clickcenter()
    elif( packet.has_key('next_game_flag') ):
        if( packet.get('next_game_flag') ):
            if( packet.get('result')=='win' ):
                print "win"
                print "続行しますか？ NextCard = ",
                card1 = xpc.listToCardClass(packet, 'card_first')
                card2 = xpc.listToCardClass(packet, 'card_second')
                payMedal = int(packet.get('pay_medal'))
                reamRound = 10-int(packet.get('turn'))
                doubleup = pokerDoubleUp.DoubleUp(card1,card2,payMedal,reamRound)
                print doubleup.card2.num
                if( doubleup.isNextDoubleUp() ):
                    print "YES"
                    #YESをクリック
                    Sleep(1000)
                    operation.clickright()
                else:
                    print "NO"
                    #NOをクリック
                    Sleep(1000)
                    operation.clickleft()
            elif( packet.get('result')=='draw' ):
                print "draw"
                print "続行しますか？ NextCard = ",
                card1 = xpc.listToCardClass(packet, 'card_first')
                card2 = xpc.listToCardClass(packet, 'card_second')
                payMedal = int(packet.get('pay_medal'))
                reamRound = 10-int(packet.get('turn'))
                doubleup = pokerDoubleUp.DoubleUp(card1,card2,payMedal,reamRound)
                print doubleup.card2.num
                if( doubleup.isNextDoubleUp() ):
                    print "YES"
                    #YESをクリック
                    Sleep(1500)
                    operation.clickright()
                else:
                    print "NO"
                    #NOをクリック
                    Sleep(1500)
                    operation.clickleft()

            elif( packet.get('result')=='lose' ):
                print "lose"
                #STARTをクリック
                Sleep(1500)
                operation.clickcenter()
        elif(not packet.get('next_game_flag')):
            if( packet.get('result')=='win' ):
                print "win"
                print "ダブルアップ上限"
                #STARTをクリック
                Sleep(2000)
                operation.clickcenter()
            elif( packet.get('result')=='draw' ):
                print "draw"
                print "Error: 知らないパターン001"
                print packet
            elif( packet.get('result')=='lose' ):
                print "lose"
                print "Error: 知らないパターン002"
                print packet

    elif( packet.has_key('card_first') ):
        print "+ダブルアップ挑戦中+"
        card1 = xpc.listToCardClass(packet, 'card_first')

        payMedal = int(packet.get('pay_medal'))
        doubleup = pokerDoubleUp.DoubleUp(card1,False,payMedal,10)
        if( doubleup.judgeHiLow()=='High' ):
            print "High"
            #Highをクリック
            Sleep(1500)
            operation.clickleft()
        elif( doubleup.judgeHiLow()=='Low' ):
            print "Low"
            #Lowをクリック
            Sleep(1500)
            operation.clickright()

    elif( packet.has_key('card_list') ):
        cards = xpc.listToCardClassList(packet,'card_list')
        hands = pokerHandsClass.Hands(cards)
        print "DealtHands:",
        print hands.showCards()
        print "Hold:",
        print hands.showHoldHandPos(1)
        print "Reason:",
        print hands.showHandKeepingReason(0)
        #ホールドするカードをクリック
        #OKをクリック
        Sleep(2000)
        operation.clickcard(hands.showHoldHandPos(0))
        Sleep(100)
        operation.clickcenter()

    elif( packet.has_key('status') ):
        getMedal = packet['status'].get('get_medal')
        if( getMedal > 0):
            print "get!!!"
            #STARTをクリック
            Sleep(2000)
            operation.clickcenter()
        else:
            print "Error: 知らないパターン003"
            print packet

    elif( packet.get('errorPopFlag') ):
        print "Erorr: errorPopFlag=True"

    else:
        print "Error: 知らないパターン"
        print packet


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
