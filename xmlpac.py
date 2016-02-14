# -*- coding: utf-8 -*-
import binascii as b2a
import xml.etree.ElementTree as ET
import json
import pokerHandsClass

def xmlToPacket(filen):
    tree = ET.parse(filen)
    pacs = [u for u in tree.findall("packet")]
    return pacs

def packetToProto(pacs):
    protos = [proto for protos in pacs for proto in protos.findall("proto") if proto.get("name")=="media"]
    return protos

def protosToField(protos):
    fields = [field.find("field") for field in protos ]
    return fields

def fieldToValue(fields):
    values = [b2a.unhexlify(field.get("value")) for field in fields]
    return values

def decodeValue(values):
    decoded = [json.loads(deco.decode('utf-8')) for deco in values]
    return decoded

def selectPacket(decoded,i):
    return decoded[i]

def listToCardClass(packet,strHoge):
    card = packet[strHoge].split("_")

    if( card[0] == '1' ):
        card[0] = 's'
    elif( card[0] == '2' ):
        card[0] = 'h'
    elif( card[0] == '3' ):
        card[0] = 'd'
    elif( card[0] == '4' ):
        card[0] = 'c'
    elif( card[0] == '99' ):
        card[0] = '99'
    else:
        return False

    x = pokerHandsClass.Card( card[0],int(card[1]) )
    return x.getCard()

def listToCardClassList(packet,strHoge):
    cards = []
    for i in [1,2,3,4,5]:
        cards.append(packet[strHoge][(str(i))].split("_"))

        if( cards[i-1][0] == '1' ):
            cards[i-1][0] = 's'
        elif( cards[i-1][0] == '2' ):
            cards[i-1][0] = 'h'
        elif( cards[i-1][0] == '3' ):
            cards[i-1][0] = 'd'
        elif( cards[i-1][0] == '4' ):
            cards[i-1][0] = 'c'
        elif( cards[i-1][0] == '99' ):
            cards[i-1][0] = '99'
        else:
            return False

        cards[i-1][1] = int(cards[i-1][1])

    return cards
