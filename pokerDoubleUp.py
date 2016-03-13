# -*- coding: utf-8 -*-
import pokerHandsClass as Card

class DoubleUp:
    def __init__(self, card1,card2,payMedal,remRound):
        self.card1 = card1
        self.card2 = card2
        self.payMedal = payMedal
        self.remainingRound = remRound
        self.hiLow = False

    def setCard2(self, card2):
        self.card2 = card2

    def setPayMedal(self, payMedal):
        self.payMedal = payMedal

    def setRemainingRound(self, remRound):
        self.remainingRound = remRound

    def judgeHiLow(self):
        if(self.card1.num == 1):
            self.hiLow = u"Low"
        elif(self.card1.num > 8):
            self.hiLow = u"Low"
        elif(self.card1.num <= 8):
            self.hiLow = u"High"

        return self.hiLow

    def _probabilityWin(self,cardNum):
        if( cardNum == 1 or cardNum == 2):
            return float(12)*4/float(51)
        elif( cardNum == 13 or cardNum == 3):
            return float(11)*4/float(51)
        elif( cardNum == 12 or cardNum == 4):
            return float(10)*4/float(51)
        elif( cardNum == 11 or cardNum == 5):
            return float(9)*4/float(51)
        elif( cardNum == 10 or cardNum == 6):
            return float(8)*4/float(51)
        elif( cardNum == 9 or cardNum == 7):
            return float(7)*4/float(51)
        elif( cardNum == 8 ):
            return float(6)*4/float(51)
        else:
            return False

    def _probabllityDraw(self):
        return float(3)/float(51)

    def _calcExpectedValue(self,payMedal,remRound):
        winProb =  float(2)/float(13)*float(48+44+40+36+32+28)/float(51) +\
            float(1)/float(13)*float(24)/float(51)
        drawProb = float(1)/float(13)*float(3)/float(51)

        if(remRound==1):
            return payMedal
        #if(payMedal*2**(remainingRound+1) < 50000):
        #   return payMedal

        payMedalNext = self._calcExpectedValue(payMedal, remRound-1)
        return winProb*payMedalNext*2 + drawProb*payMedalNext

    def _calcExpectedValueNum(self,cardNum,payMedal,remRound):
        payMedalNext = self._calcExpectedValue(payMedal, remRound)
        drawExpectedValue = self._probabllityDraw() * payMedalNext
        ExpectedValue = self._probabilityWin(cardNum) * payMedalNext * 2 + drawExpectedValue
        return ExpectedValue

    def isNextDoubleUp(self):
        if( self.payMedal>= 50000):
            return False
        if( round(
              self._calcExpectedValueNum(self.card2.num,self.payMedal,self.remainingRound)/self.payMedal + self._probabllityDraw()
              ,2) >=1.0 ):
            return True
        else:
            return False

if __name__ == '__main__':
    card1 = Card.Card()
    card1.setCard(u'h', 1)
    doubleup = DoubleUp(card1,False,100,1)
    #print doubleup.judgeHiLow()
    card2 = Card.Card()
    card2.setCard(u'h', 8)
    doubleup.setCard2(card2)
    #print doubleup.isNextDoubleUp()
    #print ""
    for num in [2,3,4,5,6,7,8,9,10,11,12,13,1]:
        print u"Num:",
        print num,
        print u"Ex:",
        print doubleup._calcExpectedValueNum(num, 1500, 11)

    print u""
    for num in [2,3,4,5,6,7,8,9,10,11,12,13,1]:
        card2 = Card.Card()
        card2.setCard('s',num)
        for reamRound in [10,9,8,7,6,5,4,3,2,1]:
            for pay in [100,200,400,800,1600,3200,6400,12800,25600,51200]:
                doubleup = DoubleUp(1,card2,pay,reamRound)
                print u"Next?[",
                print doubleup.isNextDoubleUp(),
                print u"]",
                print u"Num:",
                print num,
                print u"ReamRound:",
                print reamRound,
                print u"Pay",
                print pay
