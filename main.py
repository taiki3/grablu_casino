# -*- coding: utf-8 -*-
import xmlpac as xpc
import pokerHandsClass
import operation
from pokerHandsClass import Card

def main():
    pacs = xpc.xmlToPacket("FILENAME.xml")
    protos = xpc.packetToProto(pacs)
    fields = xpc.protosToField(protos)
    values = xpc.fieldToValue(fields)
    decoded = xpc.decodeValue(values)

    for i in xrange(len(decoded)):
        packet = xpc.selectPacket(decoded,i)
        if( packet.has_key('next_game_flag') ):
            if( packet.get('next_game_flag')==True):
                print "続行しますか？ NextCard = ",
                card1 = xpc.listToCardClass(packet, 'card_first')
                card2 = xpc.listToCardClass(packet, 'card_second')
                doubleup = pokerHandsClass.DoubleUp(card1, card2)
                #print packet
                print doubleup.card2.num
                print "YES"
            elif( packet.get('next_game_flag')==False):
                print "おしまい"
        elif( packet.has_key('card_first') ):
            #ダブルアップ１回目
            print "ダブルアップ挑戦中"
            card1 = xpc.listToCardClass(packet, 'card_first')
            doubleup = pokerHandsClass.DoubleUp(card1, False)
            print doubleup.card1.num,
            if( doubleup.judgeHiLow(doubleup.card1.num)=='High' ):
                print "High"
            elif( doubleup.judgeHiLow(doubleup.card1.num)=='Low' ):
                print "Low"

        elif( packet.has_key('card_list') ):
            #cards = xpc.listToCardClassList(packet,'card_list')
            cards = [('s', 8),\
                     ('s', 13),\
                     ('c', 3),\
                     ('s', 9),\
                     ('c', 1)]
            #print cards[1].suit, cards[1].num
            print cards
            hands = pokerHandsClass.Hands(cards)
            print hands.showCards()
            print hands.showHoldHandPos(1)
            print hands.showHandKeepingReason(0)

if __name__ == '__main__':
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

