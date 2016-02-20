# -*- coding: utf-8 -*-
import numpy as np
import random
import time
import sys
import winxpgui
import win32api
import win32con
from ctypes import *
user32 = windll.user32

#予約済み変数
#g_img_x,y : chkimgがTrueの場合座標が入る
g_img_x = -1
g_img_y = -1



#指定座標を左クリック
#chkimg実行後に引数無しで実行した場合、img座標をクリック
#x : x座標
#y : y座標
def click(x = -1,y = -1,wait = 0.2):
    if(x != -1 and y != -1):
        user32.SetCursorPos(x,y)
        user32.mouse_event(0x2,0,0,0,0) #クリックする
        sleep(wait)
        user32.mouse_event(0x4,0,0,0,0) #クリックを放す
        return(True)
    '''
    else:
        #img座標に数値が入っていた場合
        if(g_img_x != -1 and g_img_y != -1):
            x = g_img_x
            y = g_img_y
            user32.SetCursorPos(x,y)
            user32.mouse_event(0x2,0,0,0,0) #クリックする
            sleep(wait)
            user32.mouse_event(0x4,0,0,0,0) #クリックを放す
            return(True)
        else:
            return(False)
    '''

#指定座標にカーソル移動
#chkimg実行後に引数無しで実行した場合、img座標に移動
#x : x座標
#y : y座標
def mmv(x = -1,y = -1):
    if(x != -1 and y != -1):
        user32.SetCursorPos(x,y)
        return(True)
    else:
        if(g_img_x != -1 and g_img_y != -1):
            x = g_img_x
            y = g_img_y
            user32.SetCursorPos(x,y)
            return(True)
        else:
            return(False)

#キーコードを指定してキー入力
#keycode : キーコード
def kbd(keycode):
    user32.keybd_event(keycode,0,0,0)
    sleep(0.2)
    user32.keybd_event(keycode,0,0x2,0)


#処理待機
#wait : ミリ秒指定可
def sleep(wait):
    t = int(wait *1000)
    win32api.Sleep(t)
    #time.sleep(wait)

#getid - EnumWindows用コールバック関数
def proc(hwnd,ar):
    title = winxpgui.GetWindowText(hwnd)
    #print title
    #test,enco = conv_encoding(title)
    #print "title:"+title.decode('shift_jis').encode('utf-8')
    #print "test:"+test
    #print "enco:"+enco
    #win32api.MessageBox(0, title, u"てすと", win32con.MB_OK | win32con.MB_ICONINFORMATION)
    #title.decode('utf-8').encode('iso-2022-jp')
    #title.decode('iso-2022-jp').encode('utf-8')
    #print simple_chardet(title)
    #win32api.MessageBox(0, title, u"てすと", win32con.MB_OK | win32con.MB_ICONINFORMATION)
    if ar[0] in title:
        #print (hwnd, title)
        ar[1].append(hwnd)
    return 1

#titleをウィンドウタイトルに含むウィンドウのウィンドウハンドルを返します
#title : 検索に使うタイトル
#n : 何番目のウィンドウハンドルを返すか
def getid(title,n = 0):
    hwnds = []
    try:
        winxpgui.EnumWindows(proc,[title,hwnds])
    except:
        raise
    return hwnds[n]


#直接クリック情報を送ります
#hwnd : ウィンドウハンドル
#x : x座標
#y : y座標
#pbtn : 送るクリック情報 L or lで左クリック,R or rで右クリック
def PostClick(hwnd,x,y,pbtn = "L"):
    #WM_LBUTTONDOWN = 0x0201
    #WM_LBUTTONUP = 0x0202
    #WM_RBUTTONDOWN = 0x0204
    #WM_RBUTTONUP = 0x0205
    if pbtn == "L" or "l":
        sbtn = 0x0201
        ebtn = 0x0202
    elif pbtn == "R" or "r":
        sbtn = 0x0204
        ebtn = 0x0205

    # x,y => lParam
    point = y * int('0xffff',16) + x
    winxpgui.PostMessage(hwnd, sbtn, 0, point) # button down
    sleep(0.2)
    winxpgui.PostMessage(hwnd, ebtn, 0, point)   # button up