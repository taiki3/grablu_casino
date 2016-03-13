# -*- coding: utf-8 -*-
import winxpgui
import win32api
import win32con
import random

def clickHigh():
    _clickLeftButton()

def clickLow():
    _clickRightButton()

def clickYes():
    _clickRightButton()

def clickNo():
    _clickLeftButton()

def clickStart():
    _clickCenterButton()

def clickOK():
    _clickCenterButton()

def clickReload():
    hWnd = getGraBluWindow()
    size = winxpgui.GetClientRect(hWnd)
    x = int(size[2]*0.75)
    y = 560
    _clickPos(hWnd, x, y)

def sleepPlusRandom(wait,rangeMax):
    if( rangeMax == 0 ):
        win32api.Sleep(wait)
    else:
        waitTime = random.randrange(wait,wait+rangeMax)
        win32api.Sleep(waitTime)

def clickHoldCard(changeFlag):
    hWnd = getGraBluWindow()
    size = winxpgui.GetClientRect(hWnd)
    x = size[2]/2
    y = int(x * float(260)/float(175))
    cardImgSize = int(x * float(55)/float(175))
    for i in range(0,5):
        if( changeFlag[i]==True ):
            _clickPos(hWnd, x+(i-2)*cardImgSize, y)

def _clickPos(hWnd,x,y):
    XYpos= win32api.MAKELONG(x,y)
    win32api.SendMessage(hWnd, win32con.WM_LBUTTONDOWN,0,XYpos)
    win32api.SendMessage(hWnd, win32con.WM_LBUTTONUP,0,XYpos)

def _clickLeftButton():
    hWnd = getGraBluWindow()
    size = winxpgui.GetClientRect(hWnd)
    center = size[2]/2
    x = center - int(center * float(50)/float(175))
    y = int(center * float(400)/float(175))
    _clickPos(hWnd,x,y)

def _clickRightButton():
    hWnd = getGraBluWindow()
    size = winxpgui.GetClientRect(hWnd)
    center = size[2]/2
    x = center + int(center * float(50)/float(175))
    y = int(center * float(400)/float(175))
    _clickPos(hWnd,x,y)

def _clickCenterButton():
    hWnd = getGraBluWindow()
    size = winxpgui.GetClientRect(hWnd)
    center = size[2]/2
    x = center
    y = int(center * float(400)/float(175))
    _clickPos(hWnd,x,y)

def getGraBluWindow():
    title = u"グランブルーファンタジー[ChromeApps版]"
    hWnd = 0

    try:
        hWnd = winxpgui.FindWindow(0,title)
    except:
        print u"no window"
        return False
    return hWnd

if __name__ == "__main__":
    pass
    #flag = (True,True,True,False,True)
    #clickHoldCard(flag)
    clickOK()
