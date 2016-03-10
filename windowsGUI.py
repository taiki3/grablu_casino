# -*- coding: utf-8 -*-
import sys
from windowsForm import *
import ConfigParser
import packetDumpClass
import pokerReadGameData
import pokerHandsClass
import operation
import win32gui
import winxpgui
from PyQt4.Qt import QRect, QTime
import subprocess
import random
import os
import datetime

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon( QtGui.QIcon(u'icons/256x256.png') )

        self.isRunProgram = False
        self.getTotalMedal = 0
        self.countGame = 0
        self.countGameWin = 0
        self.packetTimer = QtCore.QTimer()
        self.packetTimer.timeout.connect(self.readPacket)
        self.packetTimer.setInterval(30)
        self.pDump = packetDumpClass.PacketDump()
        self.hands = pokerHandsClass.Hands()
        self.operatingStartTime = datetime.datetime.now()
        self.operatingTime = datetime.timedelta(0)
        self.opeTimer = QtCore.QTimer()
        self.opeTimer.timeout.connect(self.operatingTimeUpdate)
        self.opeTimer.setInterval(10)
        self.toTimer = QtCore.QTimer()
        self.toTimer.timeout.connect(self.packetTimeOut)
        self.toTimer.setInterval(15*1000)

        self.scheduleTimer = QtCore.QTimer()
        self.scheduleTimer.setInterval(10*1000)
        self.scheduleTimer.timeout.connect(self.scheduleRun)
        self.scheduleTimer.start()

        self.clickTimer = QtCore.QTimer()
        self.clickTimer.timeout.connect(self.delayClick)
        self.clickPosStr = u""
        self.reloadTimer = QtCore.QTimer()
        self.reloadTimer.setInterval(30*60*1000)
        self.reloadTimer.timeout.connect(self.reloadUpdate)

        deviceDict = self.pDump.getDeviceDict()
        for u in deviceDict:
            self.ui.comboBoxDevice.addItem(deviceDict[u])
        self.ui.comboBoxDevice.activated.connect(self.selectDevice)

        inifile = ConfigParser.RawConfigParser()
        if( os.path.isfile(u'config.ini') ):
            inifile.read(u'config.ini')
            left = int( inifile.get(u'window',u'left') )
            top = int( inifile.get(u'window',u'top') )
            width = int( inifile.get(u'window',u'width') )
            height = int( inifile.get(u'window',u'height') )
            rect = QRect(left,top,width,height)
            self.setGeometry(rect)
            self.nDeviceNum = int( inifile.get(u'device', u'number') )
            self.nDevice = self.pDump.selectDevice( self.nDeviceNum )
            self.ui.comboBoxDevice.setCurrentIndex(self.nDeviceNum)
            self.waitAdjust = int( inifile.get(u'wait', u'adjust') )
            self.ui.spinBox_waitAdjust.setValue( self.waitAdjust )
            self.ui.verticalSlider_waitAdjust.setValue( self.waitAdjust )
            self.waitRandomRangeMax = int( inifile.get(u'wait', u'randam_range') )
            self.ui.spinBox_waitRandom.setValue( self.waitRandomRangeMax )
            self.ui.verticalSlider_waitRandom.setValue( self.waitRandomRangeMax )
            self.ui.lineEdit_GoalMedal.setText( inifile.get(u'goal',u'medal') )
            StartTime1 = QTime( int(inifile.get(u'schedule',u'start1_h')) , \
                                int(inifile.get((u'schedule'),u'start1_m')) )
            self.ui.timeEdit_Start1.setTime( StartTime1 )
            EndTime1 = QTime( int(inifile.get(u'schedule',u'end1_h')), \
                              int(inifile.get((u'schedule'),u'end1_m')) )
            self.ui.timeEdit_End1.setTime( EndTime1 )
            StartTime2 = QTime( int(inifile.get(u'schedule',u'start2_h')), \
                                int(inifile.get((u'schedule'),u'start2_m')) )
            self.ui.timeEdit_Start2.setTime( StartTime2 )
            EndTime2 = QTime( int(inifile.get(u'schedule',u'end2_h')), \
                              int(inifile.get((u'schedule'),u'end2_m')) )
            self.ui.timeEdit_End2.setTime( EndTime2 )
        else:
            self.nDevice = False
            self.nDeviceNum = 0
            self.waitAdjust = 0
            self.waitRandomRangeMax = 0

    def selectDevice(self,iNum):
        if(iNum!=0):
            self.nDevice = self.pDump.selectDevice(iNum)
            self.nDeviceNum = iNum
        else:
            self.nDevice = False
            self.nDeviceNum = 0

    def changeWaitAdjust(self):
        self.waitAdjust = self.ui.verticalSlider_waitAdjust.value()

    def changeWaitRandom(self):
        self.waitRandomRangeMax = self.ui.verticalSlider_waitRandom.value()

    def clearInfo(self):
        self.operatingStartTime = datetime.datetime.now()
        self.operatingTime = datetime.timedelta(0)
        self.getTotalMedal = 0
        self.countGame = 0
        self.countGameWin = 0
        self.operatingTimeUpdate()

    def operatingTimeUpdate(self):
        deltaTime = datetime.datetime.now() - self.operatingStartTime
        operatingTimeHour = (deltaTime.seconds+self.operatingTime.seconds)/3600
        operatingTimeMinute = ((deltaTime.seconds+self.operatingTime.seconds)%3600) /60
        operatingTimeSecond = (deltaTime.seconds+self.operatingTime.seconds)%60
        oTimeStr = str( u"{0:02d}".format(operatingTimeHour) ) + u":" + \
          str( u"{0:02d}".format(operatingTimeMinute) ) + u":" + \
          str( u"{0:02d}".format(operatingTimeSecond) ) + u" [HH:MM:SS]"
        self.ui.label_operatingTime.setText(oTimeStr)
        if((deltaTime.seconds+self.operatingTime.seconds)!=0):
            hWageText = str( u'%09.2f' % (self.getTotalMedal/float(deltaTime.seconds+self.operatingTime.seconds)*3600) ) + u" [Medal/Hour]"
            self.ui.label_hourlyWage.setText( hWageText )
        else:
            self.ui.label_hourlyWage.setText(u'000000.00 [Medal/Hour]')
        self.ui.label_getMedal.setText( str(self.getTotalMedal) + u" [Medal]" )
        self.ui.label_countGame.setText( str(self.countGame) + u" [ 回 ]")
        self.ui.label_countGameWin.setText( str(self.countGameWin) + u" [ 回 ]")

    def scheduleRun(self):
        nowTime = datetime.datetime.now()
        if(not self.isRunProgram):
            if( self.ui.checkBox_Schedule1.isChecked() ):
                if( nowTime.hour == self.ui.timeEdit_Start1.time().hour() and \
                    nowTime.minute == self.ui.timeEdit_Start1.time().minute() ):
                        self.ui.textEdit.append(u'スケジュール1開始')
                        self.runProgram()
                        self.reloadClick()
                        return

            if( self.ui.checkBox_Schedule2.isChecked() ):
                if( nowTime.hour == self.ui.timeEdit_Start2.time().hour() and \
                    nowTime.minute == self.ui.timeEdit_Start2.time().minute() ):
                        self.ui.textEdit.append(u'スケジュール2開始')
                        self.runProgram()
                        self.reloadClick()
                        return
        else:
            if( self.ui.checkBox_Schedule1.isChecked() ):
                if( nowTime.hour == self.ui.timeEdit_End1.time().hour() and \
                    nowTime.minute == self.ui.timeEdit_End1.time().minute() ):
                        self.ui.textEdit.append(u'スケジュール1終了')
                        self.pauseProgram()
                        return

            if( self.ui.checkBox_Schedule2.isChecked() ):
                if( nowTime.hour == self.ui.timeEdit_End2.time().hour() and \
                    nowTime.minute == self.ui.timeEdit_End2.time().minute() ):
                        self.ui.textEdit.append(u'スケジュール2終了')
                        self.pauseProgram()
                        return

    def shortcutGrablu(self):
        if( not operation.getGraBluWindow() ):
            cmd = u"start chrome.exe --profile-directory=Default --app-id=eablgejicbklomgaiclcolfilbkckngf"
            subprocess.call(cmd, shell=True)
        else:
            self.ui.textEdit.append(u"多重起動はできません")

    def _setWaitTime(self,wait):
        if( self.waitRandomRangeMax==0 ):
            self.clickTimer.setInterval(wait)
            self.clickTimer.start()
            self.packetTimer.stop()
        else:
            self.clickTimer.setInterval( random.randrange(wait,wait+self.waitRandomRangeMax) )
            self.clickTimer.start()
            self.packetTimer.stop()

    def delayClick(self):
        print "Click!!!!"
        self.packetTimer.start()
        if( self.clickPosStr==u'High' ):
            operation.clickHigh()
        elif( self.clickPosStr==u'Low' ):
            operation.clickLow()
        elif( self.clickPosStr==u'Yes' ):
            operation.clickYes()
        elif( self.clickPosStr==u'No' ):
            operation.clickNo()
        elif( self.clickPosStr==u'Start' ):
            operation.clickStart()
        elif( self.clickPosStr==u'Ok' ):
            operation.clickOK()
        elif( self.clickPosStr==u'Hold' ):
            operation.clickHoldCard(self.hands.showHoldHandPos(0))
            operation.clickOK()

        self.clickTimer.stop()

    def runProgram(self):
        if(self.isRunProgram):
            self.pauseProgram()
            return

        if(not operation.getGraBluWindow()):
            self.ui.textEdit.append(u'グラブルが起動されていません')
            return

        if(self.nDeviceNum == 0):
            self.ui.textEdit.append(u"デバイスが選択されていません")
            return

        self.ui.textEdit.append(u'プログラム開始')
        self.pDump.runPacketDump(self.nDevice)
        self.operatingStartTime = datetime.datetime.now()
        self.packetTimer.start()
        self.opeTimer.start()
        self.reloadTimer.start()

        self.isRunProgram = True
        self.ui.pushButtonRun.setText(u"停止")
        self.toTimer.start()

    def reloadClick(self):
        operation.clickReload()
        self.clickTimer.stop()
        self.toTimer.start()
        self.packetTimer.start()

    def reloadUpdate(self):
        if( self.ui.checkBox_Reload.isChecked() ):
            self.ui.textEdit.append(u"画像認証回避のためのリロード")
            self.reloadClick()

    def packetTimeOut(self):
        self.ui.textEdit.append(u"タイムアウトしました")
        self.reloadClick()

    def pauseProgram(self):
        self.isRunProgram = False
        self.ui.textEdit.append(u'プログラム停止')
        self.operatingTime = self.operatingTime + datetime.datetime.now() - self.operatingStartTime
        self.clickTimer.stop()
        self.toTimer.stop()
        self.opeTimer.stop()
        self.packetTimer.stop()
        self.reloadTimer.stop()
        self.pDump.closePacketDump()

        self.ui.pushButtonRun.setText(u"実行")
        return

    def readPacket(self):
        res = self.pDump.getPacket()
        if(res==0):
            self.packetTimeOut()
            return
        if(res>0):
            gameData = self.pDump.packetToGameData()
            if( gameData ):
                self.toTimer.start()
                gameStatus = pokerReadGameData.readGameData(gameData)
                if( gameStatus.has_key(u'status') ):
                    if( gameStatus.get(u'status')==u'ERROR_POP_FLAG_TRUE' ):
                        self.ui.textEdit.append( gameStatus.get(u'status') )
                        self.ui.textEdit.append( gameStatus.get(u'data') )
                        return
                    elif( gameStatus.get(u'status')==u'MYPAGE_LOADING' or \
                        gameStatus.get(u'status')==u'MSGDATA_LOADING' or \
                        gameStatus.get(u'status')==u'MP3DATA_LOADING' or \
                        gameStatus.get(u'status')==u'ANYDATA_LOADING' or \
                        gameStatus.get(u'status')==u'CHECK_PLAYING_OTHER_GAMES' or \
                        gameStatus.get(u'status')==u'WELCOME_CASINO' ):
                        #self.ui.textEdit.append( gameStatus.get(u'status') )
                        return
                    elif( gameStatus.get(u'status')==u'POKER_START' ):
                        self.ui.textEdit.append( u'Poker start' )
                        self._setWaitTime(500)
                        self.clickPosStr = u'Start'
                        return

                    elif( gameStatus.get(u'status')==u'GAME_START'):
                        self.hands = gameStatus.get(u'Hands')
                        self.ui.textEdit.append( u"Dealt")
                        self.ui.textEdit.append( u"├Hands: "+self.hands.showCardsStr() )
                        self.ui.textEdit.append( u'├Hold: '+self.hands.showHoldHandPosStr(0) )
                        self.ui.textEdit.append( u'└Reason: '+self.hands.showHandKeepingReason(0) )
                        self._setWaitTime(2000+self.waitAdjust)
                        self.clickPosStr=u'Hold'
                        self.getTotalMedal -= 100
                        self.countGame+=1
                        return

                    elif( gameStatus.get(u'status')==u'GAME_WIN' ):
                        self.hands = gameStatus.get(u'Hands')
                        self.ui.textEdit.append( u'Win' )
                        self.ui.textEdit.append( u"├Result: "+self.hands.showCardsStr() )
                        self.ui.textEdit.append( u'└Hand: '+gameStatus.get(u'hand_name' ) )
                        self._setWaitTime(2500+self.waitAdjust)
                        self.clickPosStr=u'Yes'
                        self.countGameWin+=1
                        return

                    elif( gameStatus.get(u'status')==u'RESTART_GAME_WIN' ):
                        self.hands = gameStatus.get(u'Hands')
                        self.ui.textEdit.append( u'Win' )
                        self.ui.textEdit.append( u"└Result: "+self.hands.showCardsStr() )
                        self._setWaitTime(2500+self.waitAdjust)
                        self.clickPosStr=u'Yes'
                        self.countGameWin+=1
                        return

                    elif( gameStatus.get(u'status')==u'GAME_LOSE' ):
                        self.hands = gameStatus.get(u'Hands')
                        self.ui.textEdit.append( u'Lose' )
                        self.ui.textEdit.append( u"├ResultHands: "+self.hands.showCardsStr() )
                        self.ui.textEdit.append( u'└Hand: '+gameStatus.get(u'hand_name' ) )
                        self._setWaitTime(2500+self.waitAdjust)
                        self.clickPosStr=u'Start'
                        return

                    elif( gameStatus.get(u'status')==u'DOUBLEUP_HIGH'):
                        self.ui.textEdit.append( u'DoubleUP' )
                        self.ui.textEdit.append( u'└High' )
                        self._setWaitTime(1700+self.waitAdjust)
                        self.clickPosStr=u'High'
                        return

                    elif( gameStatus.get(u'status')==u'DOUBLEUP_LOW'):
                        self.ui.textEdit.append( u'DoubleUP' )
                        self.ui.textEdit.append( u'└Low' )
                        self._setWaitTime(1700+self.waitAdjust)
                        self.clickPosStr=u'Low'
                        return

                    elif( gameStatus.get(u'status')==u'RESTART_DOUBLEUP_HIGH'  ):
                        self.ui.textEdit.append( u'DoubleUP' )
                        self.ui.textEdit.append( u'└High' )
                        self._setWaitTime(1700+self.waitAdjust)
                        self.clickPosStr=u'High'
                        return

                    elif( gameStatus.get(u'status')==u'RESTART_DOUBLEUP_LOW' ):
                        self.ui.textEdit.append( u'DoubleUP' )
                        self.ui.textEdit.append( u'└Low' )
                        self._setWaitTime(1700+self.waitAdjust)
                        self.clickPosStr=u'Low'
                        return

                    elif( gameStatus.get(u'status')==u'IS_NEXT_DOUBLEUP_YES' ):
                        doubleup = gameStatus.get(u'DoubleUp')
                        self.ui.textEdit.append( u'Remains:'+str(doubleup.remainingRound-1)+ " "+ \
                                                 u'Next:'+doubleup.card2.showCardStr() )
                        self.ui.textEdit.append( u'└Continue: YES' )
                        self._setWaitTime(1500+self.waitAdjust)
                        self.clickPosStr=u'Yes'
                        return

                    elif( gameStatus.get(u'status')==u'IS_NEXT_DOUBLEUP_NO' ):
                        doubleup = gameStatus.get(u'DoubleUp')
                        self.ui.textEdit.append( u'Remains:'+str(doubleup.remainingRound-1)+ " "+ \
                                                 u'Next:'+doubleup.card2.showCardStr() )
                        self.ui.textEdit.append( u'└Continue: NO' )
                        self._setWaitTime(1500+self.waitAdjust)
                        self.clickPosStr=u'No'
                        return

                    elif( gameStatus.get(u'status')==u'DOUBLEUP_LOSE' ):
                        self.ui.textEdit.append( u'Lose' )
                        self._setWaitTime(2000+self.waitAdjust)
                        self.clickPosStr=u'Start'
                        return

                    elif( gameStatus.get(u'status')==u'DOUBLEUP_MAX' ):
                        if( gameStatus.has_key(u'get') ):
                            getMedal = gameStatus.get(u'get')
                            self.ui.textEdit.append( u'Get '+ str(getMedal)+u' medals!' )
                            self._setWaitTime(1500+self.waitAdjust)
                            self.clickPosStr=u'Start'
                            self.getTotalMedal += getMedal
                            haveMedal = int(gameStatus.get(u'have_medal'))
                            if( self.ui.checkBox_GoalMedal.isChecked() ):
                                if( haveMedal >= int(self.ui.lineEdit_GoalMedal.text()) ):
                                    self.ui.textEdit.append( u'目標メダル数に到達しました' )
                                    self.pauseProgram()
                            return

                    elif( gameStatus.get(u'status')==u'GET_MEDAL' ):
                        if( gameStatus.has_key(u'get') ):
                            getMedal = gameStatus.get(u'get')
                            self.ui.textEdit.append( u'Get '+ str(getMedal)+u' medals!' )
                            self._setWaitTime(1500+self.waitAdjust)
                            self.clickPosStr=u'Start'
                            self.getTotalMedal += int(getMedal)
                            haveMedal = int(gameStatus.get(u'have_medal'))
                            if( self.ui.checkBox_GoalMedal.isChecked() ):
                                if( haveMedal >= int(self.ui.lineEdit_GoalMedal.text()) ):
                                    self.ui.textEdit.append( u'目標メダル数に到達しました' )
                                    self.pauseProgram()
                            return

                    elif( gameStatus.get(u'status')==u'DOUBLEUP_10ROUND_DRAW' ):
                        self.ui.textEdit.append( u'Draw' )
                        if( gameStatus.has_key(u'get') ):
                            getMedal = gameStatus.get(u'get')
                            self.ui.textEdit.append( u'Get '+ str(getMedal)+u' medals!' )
                            self._setWaitTime(1500+self.waitAdjust)
                            self.clickPosStr=u'Start'
                            self.getTotalMedal += int(getMedal)
                            haveMedal = int(gameStatus.get(u'have_medal'))
                            if( self.ui.checkBox_GoalMedal.isChecked() ):
                                if( haveMedal >= int(self.ui.lineEdit_GoalMedal.text()) ):
                                    self.ui.textEdit.append( u'目標メダル数に到達しました' )
                                    self.pauseProgram()
                            return

                    elif( gameStatus.get(u'status')==u'DOUBLEUP_10ROUND_LOSE'):
                        self.ui.textEdit.append( u'Lose' )
                        self._setWaitTime(1500+self.waitAdjust)
                        self.clickPosStr=u'Start'
                        return

                    elif( gameStatus.get(u'status')==u'UNKNOWN'):
                        self.ui.textEdit.append( u'UNKNOWN DATA' )
                        if( gameStatus.has_key(u'data') ):
                            print gameStatus.get(u'data')
                            return
                        if( gameStatus.has_key(u'num') ):
                            self.ui.textEdit.append( u'ErrorNum:'+gameStatus.get(u'num') )
                            return


    def closeEvent(self, *args, **kwargs):
        self.toTimer.stop()
        self.packetTimer.stop()
        self.opeTimer.stop()
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
        inifile.set(u'wait',u'adjust',str(self.waitAdjust))
        inifile.set(u'wait',u'randam_range',str(self.waitRandomRangeMax))
        inifile.add_section(u'goal')
        inifile.set(u'goal',u'medal',str(self.ui.lineEdit_GoalMedal.text()))
        inifile.add_section(u'schedule')
        inifile.set(u'schedule',u'start1_h',str(self.ui.timeEdit_Start1.time().hour()) )
        inifile.set(u'schedule',u'start1_m',str(self.ui.timeEdit_Start1.time().minute()) )
        inifile.set(u'schedule',u'end1_h',str(self.ui.timeEdit_End1.time().hour()) )
        inifile.set(u'schedule',u'end1_m',str(self.ui.timeEdit_End1.time().minute()) )
        inifile.set(u'schedule',u'start2_h',str(self.ui.timeEdit_Start2.time().hour()) )
        inifile.set(u'schedule',u'start2_m',str(self.ui.timeEdit_Start2.time().minute()) )
        inifile.set(u'schedule',u'end2_h',str(self.ui.timeEdit_End2.time().hour()) )
        inifile.set(u'schedule',u'end2_m',str(self.ui.timeEdit_End2.time().minute()) )

        with open(u'config.ini', u'wb') as configfile:
            inifile.write(configfile)

        return QtGui.QMainWindow.closeEvent(self, *args, **kwargs)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())