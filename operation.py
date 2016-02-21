# -*- coding: utf-8 -*-
import winxpgui
import win32api
import random
from ctypes import windll

def clickHigh():
    clickLeft()

def clickLow():
    clickRight()

def clickYes():
    clickRight()

def clickNo():
    clickLeft()

def clickStart():
    clickCenter()

def clickOK():
    clickCenter()

def sleepPlusRandom(wait):
    waitTime = random.randrange(wait,wait+1)
    win32api.Sleep(waitTime)

def clickHoldCard(changeflag):
    windowinfo = _getwindowinfo()
    if windowinfo == False:
        return(False)
    x = windowinfo[0]
    y = windowinfo[1]
    sgain = windowinfo[2]
    for i in range(0,5):
        if changeflag[i] == True:
            _click(int(x+(i-2)*55*sgain),int(y+260*sgain),0)

    win32api.Sleep(200)
    return(True)

def clickLeft():
    windowinfo = _getwindowinfo()
    if windowinfo == False:
        return(False)
    x = windowinfo[0]
    y = windowinfo[1]
    sgain = windowinfo[2]
    _click(int(x-50*sgain),int(y+400*sgain),0)

def clickRight():
    windowinfo = _getwindowinfo()
    if windowinfo == False:
        return(False)
    x = windowinfo[0]
    y = windowinfo[1]
    sgain = windowinfo[2]
    _click(int(x+50*sgain),int(y+400*sgain),0)

def clickCenter():
    windowinfo = _getwindowinfo()
    if windowinfo == False:
        return(False)
    x = windowinfo[0]
    y = windowinfo[1]
    sgain = windowinfo[2]
    _click(int(x),int(y+400*sgain),0)

def _getwindowinfo():
    try:
        #title = "グランブルーファンタジー[ChromeApps版]"
        title = "ChromeApps"
        hwnd = _getid(title,0)
    except:
        print(u"no window")
        return(False)
    rect = winxpgui.GetWindowRect(hwnd)
    size = winxpgui.GetClientRect(hwnd)
    place = winxpgui.GetWindowPlacement(hwnd)
    if place[1]!=1:
        return(False)
    x = rect[0]+size[2]/2
    y = rect[1]
    sgain = False
    if size[2] == 350:
        sgain = 1
    elif size[2] == 510:
        sgain = 1.46
    elif size[2] == 670:
        sgain = 1.9
    windowinfo = (x, y, sgain)
    return(windowinfo)

def _click(x = -1,y = -1,wait = 200):
    user32 = windll.user32
    if(x != -1 and y != -1):
        user32.SetCursorPos(x,y)
        user32.mouse_event(0x2,0,0,0,0) #クリックする
        win32api.Sleep(wait)
        user32.mouse_event(0x4,0,0,0,0) #クリックを放す
        return(True)

def _proc(hwnd,ar):
    #getid - EnumWindows用コールバック関数
    title = winxpgui.GetWindowText(hwnd)
    if ar[0] in title:
        ar[1].append(hwnd)
    return 1

def _getid(title,n = 0):
    #titleをウィンドウタイトルに含むウィンドウのウィンドウハンドルを返します
    #title : 検索に使うタイトル
    #n : 何番目のウィンドウハンドルを返すか
    hwnds = []
    try:
        winxpgui.EnumWindows(_proc,[title,hwnds])
    except:
        raise
    return hwnds[n]

if __name__ == "__main__":
    pass