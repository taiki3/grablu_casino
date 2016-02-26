# -*- coding: utf-8 -*-
import sys
from windowsForm import *
import ConfigParser
import packetDump_test
import pokerReadGameData
import pokerHandsClass
import operation
import win32gui
import winxpgui
from PyQt4.Qt import QRect
import subprocess
from _ctypes import POINTER

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.isRunProgram = False
        self.pTimer = QtCore.QTimer()
        self.pTimer.timeout.connect(self.readPacket)
        self.pDump = packetDump_test.PacketDump()
        self.hands = pokerHandsClass.Hands()

        deviceDict = self.pDump.getDeviceDict()
        for u in deviceDict:
            self.ui.comboBoxDevice.addItem(deviceDict[u])
        self.ui.comboBoxDevice.activated.connect(self.selectDevice)

        inifile = ConfigParser.RawConfigParser()
        if( inifile.read(u'config.ini') ):
            left = int( inifile.get(u'window',u'left') )
            top = int( inifile.get(u'window',u'top') )
            width = int( inifile.get(u'window',u'width') )
            height = int( inifile.get(u'window',u'height') )
            rect = QRect(left,top,width,height)
            self.setGeometry(rect)
            self.nDeviceNum = int( inifile.get(u'device', u'number') )
            self.nDevice = self.pDump.selectDevice( self.nDeviceNum )
            self.ui.comboBoxDevice.setCurrentIndex(self.nDeviceNum)
            self.waitBase = int( inifile.get(u'wait', u'base') )
            self.ui.spinBox_waitBase.setValue( self.waitBase )
            self.ui.verticalSlider_waitBase.setValue( self.waitBase )
            self.waitRandomRangeMax = int( inifile.get(u'wait', u'randam_range') )
            self.ui.spinBox_waitRandom.setValue( self.waitRandomRangeMax )
            self.ui.verticalSlider_waitRandom.setValue( self.waitRandomRangeMax )
        else:
            self.nDevice = False
            self.nDeviceNum = 0
            self.waitBase = 1000
            self.waitRandomRangeMax = 1000

    def selectDevice(self,iNum):
        if(iNum!=0):
            self.nDevice = self.pDump.selectDevice(iNum)
            self.nDeviceNum = iNum
        else:
            self.nDevice = False
            self.nDeviceNum = 0

    def changeWaitBase(self):
        self.waitBase = self.ui.verticalSlider_waitBase.value()

    def changeWaitRandom(self):
        self.waitRandomRangeMax = self.ui.verticalSlider_waitRandom.value()

    def shortcutGrablu(self):
        cmd = u"start chrome.exe --profile-directory=Default --app-id=eablgejicbklomgaiclcolfilbkckngf"
        subprocess.call(cmd, shell=True)

    def runProgram(self):
        if(self.isRunProgram):
            self.isRunProgram = False
            self.ui.textEdit.append(u'プログラム停止')
            self.pTimer.stop()
            self.pDump.closePacketDump()

            self.ui.pushButtonRun.setText(u"実行")
            return

        if(self.nDeviceNum == 0):
            self.ui.textEdit.append(u"デバイスが選択されていません")
            return

        self.ui.textEdit.append(u'プログラム開始')
        self.pDump.runPacketDump(self.nDevice)

        self.pTimer.start(20)

        self.isRunProgram = True
        self.ui.pushButtonRun.setText(u"停止")


    def readPacket(self):
        res = self.pDump.getPacket()
        if(res==0):
            print u"タイムアウト"
            #self.timer.stop()
            #self.timer.timeout.disconnect()
            return
        if(res>0):
            gameData = self.pDump.packetToGameData()
            if( gameData ):
                gameStatus = pokerReadGameData.readGameData(gameData)
                if( gameStatus.has_key(u'status') ):
                    if( gameStatus.get(u'status')==u'ERROR_POP_FLAG_TRUE' ):
                        self.ui.textEdit.append( gameStatus.get(u'status') )
                        self.ui.textEdit.append( gameStatus.get(u'data') )
                    if( gameStatus.get(u'status')==u'MYPAGE_LOADING' or \
                        gameStatus.get(u'status')==u'MSGDATA_LOADING' or \
                        gameStatus.get(u'status')==u'MP3DATA_LOADING' or \
                        gameStatus.get(u'status')==u'ANYDATA_LOADING' or \
                        gameStatus.get(u'status')==u'CHECK_PLAYING_OTHER_GAMES' or \
                        gameStatus.get(u'status')==u'WELCOME_CASINO' ):
                        self.ui.textEdit.append( gameStatus.get(u'status') )
                    if( gameStatus.get(u'status')==u'POKER_START' ):
                        self.ui.textEdit.append( u'Poker start' )
                        operation.sleepPlusRandom(10,self.waitRandomRangeMax)
                        operation.clickStart()

                    if( gameStatus.get(u'status')==u'GAME_START'):
                        self.hands = gameStatus.get(u'Hands')
                        self.ui.textEdit.append( u"Dealt")
                        self.ui.textEdit.append( u"├Hands: "+self.hands.showCardsStr() )
                        self.ui.textEdit.append( u'├Hold: '+self.hands.showHoldHandPosStr(0) )
                        self.ui.textEdit.append( u'└Reason: '+self.hands.showHandKeepingReason(0) )
                        self.ui.textEdit.update()
                        operation.sleepPlusRandom(self.waitBase*3,self.waitRandomRangeMax)
                        operation.clickHoldCard(self.hands.showHoldHandPos(0))
                        operation.clickOK()
                    if( gameStatus.get(u'status')==u'GAME_WIN' ):
                        self.hands = gameStatus.get(u'Hands')
                        self.ui.textEdit.append( u'Win' )
                        self.ui.textEdit.append( u"├Result: "+self.hands.showCardsStr() )
                        self.ui.textEdit.append( u'└Hand: '+gameStatus.get(u'hand_name' ) )
                        operation.sleepPlusRandom(int(self.waitBase*2.5),self.waitRandomRangeMax)
                        operation.clickYes()
                    if( gameStatus.get(u'status')==u'GAME_LOSE' ):
                        self.hands = gameStatus.get(u'Hands')
                        self.ui.textEdit.append( u'Lose' )
                        self.ui.textEdit.append( u"├ResultHands: "+self.hands.showCardsStr() )
                        self.ui.textEdit.append( u'└Hand: '+gameStatus.get(u'hand_name' ) )
                        operation.sleepPlusRandom(int(self.waitBase*2.5),self.waitRandomRangeMax)
                        operation.clickStart()
                    if( gameStatus.get(u'status')==u'DOUBLEUP_HIGH'):
                        self.ui.textEdit.append( u'DoubleUP' )
                        self.ui.textEdit.append( u'└High' )
                        operation.sleepPlusRandom(int(self.waitBase*1.5),self.waitRandomRangeMax)
                        operation.clickHigh()
                    if( gameStatus.get(u'status')==u'DOUBLEUP_LOW'):
                        self.ui.textEdit.append( u'DoubleUP' )
                        self.ui.textEdit.append( u'└Low' )
                        operation.sleepPlusRandom(int(self.waitBase*1.5),self.waitRandomRangeMax)
                        operation.clickLow()
                    if( gameStatus.get(u'status')==u'RESTART_DOUBLEUP_HIGH'  ):
                        self.ui.textEdit.append( u'DoubleUP' )
                        self.ui.textEdit.append( u'└High' )
                        operation.sleepPlusRandom(self.waitBase*2,self.waitRandomRangeMax)
                        operation.clickHigh()
                    if( gameStatus.get(u'status')==u'RESTART_DOUBLEUP_LOW' ):
                        self.ui.textEdit.append( u'DoubleUP' )
                        self.ui.textEdit.append( u'└Low' )
                        operation.sleepPlusRandom(self.waitBase*2,self.waitRandomRangeMax)
                        operation.clickLow()

                    if( gameStatus.get(u'status')==u'IS_NEXT_DOUBLEUP_YES' ):
                        doubleup = gameStatus.get(u'DoubleUp')
                        self.ui.textEdit.append( u'Remains:'+str(doubleup.remainingRound-1)+ " "+ \
                                                 u'Next:'+doubleup.card2.showCardStr() )
                        self.ui.textEdit.append( u'└Continue: YES' )
                        operation.sleepPlusRandom(int(self.waitBase*1.5),self.waitRandomRangeMax)
                        operation.clickYes()
                    if( gameStatus.get(u'status')==u'IS_NEXT_DOUBLEUP_NO' ):
                        doubleup = gameStatus.get(u'DoubleUp')
                        self.ui.textEdit.append( u'Remains:'+str(doubleup.remainingRound-1)+ " "+ \
                                                 u'Next:'+doubleup.card2.showCardStr() )
                        self.ui.textEdit.append( u'└Continue: NO' )
                        operation.sleepPlusRandom(int(self.waitBase*1.5),self.waitRandomRangeMax)
                        operation.clickNo()
                    if( gameStatus.get(u'status')==u'DOUBLEUP_LOSE' ):
                        self.ui.textEdit.append( u'Lose' )
                        operation.sleepPlusRandom(int(self.waitBase*1.5),self.waitRandomRangeMax)
                        operation.clickStart()
                    if( gameStatus.get(u'status')==u'DOUBLEUP_MAX' ):
                        if( gameStatus.has_key(u'get') ):
                            getMedal = gameStatus.get(u'get')
                            self.ui.textEdit.append( u'get '+ str(getMedal)+u' medals!' )
                            operation.sleepPlusRandom(self.waitBase*2,self.waitRandomRangeMax)
                            operation.clickStart()
                    if( gameStatus.get(u'status')==u'GET_MEDAL' ):
                        if( gameStatus.has_key(u'get') ):
                            getMedal = gameStatus.get(u'get')
                            self.ui.textEdit.append( u'get '+ str(getMedal)+u' medals!' )
                            operation.sleepPlusRandom(self.waitBase*2,self.waitRandomRangeMax)
                            operation.clickStart()
                    if( gameStatus.get(u'status')==u'DOUBLEUP_10ROUND_DRAW' ):
                        self.ui.textEdit.append( u'Draw' )
                        operation.sleepPlusRandom(self.waitBase*2,self.waitRandomRangeMax)
                        operation.clickStart()
                    if( gameStatus.get(u'status')==u'DOUBLEUP_10ROUND_LOSE'):
                        self.ui.textEdit.append( u'Lose' )
                        operation.sleepPlusRandom(self.waitBase*2,self.waitRandomRangeMax)
                        operation.clickStart()
                    if( gameStatus.get(u'status')==u'UNKNOWN'):
                        self.ui.textEdit.append( u'UNKNOWN DATA' )
                        if( gameStatus.has_key(u'data') ):
                            self.ui.textEdit.append( gameStatus.get(u'data') )
                        if( gameStatus.has_key(u'num') ):
                            self.ui.textEdit.append( u'ErrorNum:'+gameStatus.get(u'num') )

    def closeEvent(self, *args, **kwargs):
        myHwnd = winxpgui.FindWindow(0,unicode(self.windowTitle()))
        left, top, right, bottom = win32gui.GetWindowRect(myHwnd)
        cLeft,cTop,cRight,cBottom = win32gui.GetClientRect(myHwnd)
        inifile = ConfigParser.SafeConfigParser()
        inifile.add_section(u'window')
        inifile.set(u'window',u'left',str(left))
        inifile.set(u'window',u'top',str(top))
        inifile.set(u'window',u'width',str(cRight - cLeft))
        inifile.set(u'window',u'height',str(cBottom - cTop))
        inifile.add_section(u'device')
        inifile.set(u'device',u'number',str(self.nDeviceNum))
        inifile.add_section(u'wait')
        inifile.set(u'wait',u'base',str(self.waitBase))
        inifile.set(u'wait',u'randam_range',str(self.waitRandomRangeMax))

        with open(u'config.ini', u'wb') as configfile:
            inifile.write(configfile)

        return QtGui.QMainWindow.closeEvent(self, *args, **kwargs)
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())