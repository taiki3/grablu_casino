# -*- coding: utf-8 -*-
import pokerHandsClass as Card

class DoubleUp:
    def __init__(self, card1,card2,payMedal,remRound):
        self.card1 = card1
        self.card2 = card2
        self.payMedal = payMedal
        self.remainningRound = remRound
        self.hiLow = False

    def setCard2(self, card2):
        self.card2 = card2

    def setPayMedal(self, payMedal):
        self.payMedal = payMedal

    def setRemainningRound(self, remRound):
        self.remainningRound = remRound

    def judgeHiLow(self):
        if(self.card1.num == 1):
            self.hiLow = "Low"
        elif(self.card1.num > 8):
            self.hiLow = "Low"
        elif(self.card1.num <= 8):
            self.hiLow = "High"

        return self.hiLow

    def probabilityWin(self,cardNum):
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

    def probabllityDraw(self):
        return float(3)/float(51)

    def calcExpectedValue(self,payMedal,remainingRound):
        winProb =  float(2)/float(13)*float(48+44+40+36+32+28)/float(51) +\
            float(1)/float(13)*float(24)/float(51)
        drawProb = float(1)/float(13)*float(3)/float(51)

        if(remainingRound==1):
            return payMedal
        if(payMedal*2**(remainingRound+1) <  50000):
            return payMedal

        payMedalNext = self.calcExpectedValue(payMedal, remainingRound-1)
        return winProb*payMedalNext*2 + drawProb*payMedalNext

    def calcExpectedValueNum(self,cardNum,payMedal,remainingRound):
        payMedalNext = self.calcExpectedValue(payMedal, remainingRound)
        drawExpectedValue = self.probabllityDraw() * payMedalNext
        ExpectedValue = self.probabilityWin(cardNum) * payMedalNext * 2 + drawExpectedValue
        return ExpectedValue

    def isNextDoubleUp(self):
        if( self.payMedal>= 50000):
            return False
        if( round(
              self.calcExpectedValueNum(self.card2.num,self.payMedal,self.remainningRound)/self.payMedal + self.probabllityDraw()
              ,2) >=2.0 ):
            return True
        else:
            return False

if __name__ == '__main__':
    card1 = Card.Card('h', 1)
    doubleup = DoubleUp(card1,False,100,1)
    print doubleup.judgeHiLow()
    card2 = Card.Card('h', 8)
    doubleup.setCard2(card2)
    print doubleup.isNextDoubleUp()

    print ""
    for num in [2,3,4,5,6,7,8,9,10,11,12,13,1]:
        print "Num:",
        print num,
        print "Ex:",
        print doubleup.calcExpectedValueNum(num, 800, 2)/800

    print ""
    for num in [2,3,4,5,6,7,8,9,10,11,12,13,1]:
        card2 = Card.Card('s',num)
        for reamRound in [10,9,8,7,6,5,4,3,2,1]:
            for pay in [100,200,400,800,1600,3200,6400,12800,25600,51200]:
                doubleup = DoubleUp(1,card2,pay,reamRound)
                print "Next?[",
                print doubleup.isNextDoubleUp(),
                print "]",
                print "Num:",
                print num,
                print "ReamRound:",
                print reamRound,
                print "Pay",
                print pay
