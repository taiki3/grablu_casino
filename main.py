# -*- coding: utf-8 -*-
import xmlpac as xpc
import pokerHandsClass
import operation
import pokerDoubleUp

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

def main():
    pacs = xpc.xmlToPacket("FILENAME.xml")
    protos = xpc.packetToProto(pacs)
    fields = xpc.protosToField(protos)
    values = xpc.fieldToValue(fields)
    decoded = xpc.decodeValue(values)

    for i in xrange(len(decoded)):
        packet = xpc.selectPacket(decoded,i)
        if( packet.has_key('card_list') and packet.has_key('result') ):
            if( packet.get('result')=='win' ):
                print "ダブルアップに挑戦しますか？ YES!"
                #YESをクリック
            elif( packet.get('result')=='lose' ):
                if( packet.has_key('hand') ):
                    cards = xpc.listToCardClassList(packet,'card_list')
                    hands = pokerHandsClass.Hands(cards)
                    print "ResultHands:",
                    print hands.showCards()
                    print "Result:",
                    print handName(packet.get('hand_id'))
                    #STARTをクリック

        elif( packet.get('next_game_flag')==True ):
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
                else:
                    print "NO"
                    #NOをクリック
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
                else:
                    print "NO"
                    #NOをクリック
            elif( packet.get('result')=='lose' ):
                print "lose"
                #STARTをクリック

        elif( packet.get('next_game_flag')==False ):
            if( packet.get('result')=='win' ):
                print "win"
                print "ダブルアップ上限"
                #STARTをクリック
            elif( packet.get('result')=='draw' ):
                print "draw"
                print "Error: 知らないパパターン"
                print packet
            elif( packet.get('result')=='lose' ):
                print "lose"
                print "Error: 知らないパパターン"
                print packet

        elif( packet.has_key('card_first') ):
            print "+ダブルアップ挑戦中+"
            card1 = xpc.listToCardClass(packet, 'card_first')

            payMedal = int(packet.get('pay_medal'))
            doubleup = pokerDoubleUp.DoubleUp(card1,False,payMedal,10)
            if( doubleup.judgeHiLow()=='High' ):
                print "High"
                #Highをクリック
            elif( doubleup.judgeHiLow()=='Low' ):
                print "Low"
                #Lowをクリック

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

        elif( packet.has_key('get_medal') ):
            print "get!!!"
            #STARTをクリック

        elif( packet.has_key('errorPopFlag')):
            print "Erorr: errorPopFlas=True"

        else:
            print "Error: 知らないパパターン"
            print packet


if __name__ == '__main__':
    main()
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
