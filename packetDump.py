# -*- coding: utf-8 -*-
from ctypes import *
from winpcapy import *
import sys
import string
import platform
import pokerReadGameData
import win32api
from win32con import *
import dpkt,socket
import json
import gzip
from StringIO import StringIO

if platform.python_version()[0] == "3":
    raw_input=input
LINE_LEN=16
alldevs=POINTER(pcap_if_t)()
d=POINTER(pcap_if_t)
fp=pcap_t
errbuf= create_string_buffer(PCAP_ERRBUF_SIZE)
header=POINTER(pcap_pkthdr)()
pkt_data=POINTER(c_ubyte)()

def packetToGameData(packet):
    eth = dpkt.ethernet.Ethernet(packet)
    if( type(eth.data) == dpkt.ip.IP ):
        ip = eth.data
        src = socket.inet_ntoa(ip.src)
        if( src==socket.gethostbyname(u'gbf.game.mbga.jp') ):
            if( type(ip.data) == dpkt.tcp.TCP ):
                tcp = ip.data
                if( len(tcp.data)>0 ):
                    try:
                        http = dpkt.http.Response(tcp.data)
                        jsonData = gzip.GzipFile( fileobj=StringIO(http.body) ).read()
                        if( http.headers[u'content-type'] != u'application/json' ):
                            return False
                        if(not u"{" in jsonData ):
                            return False
                        gameData = json.loads(jsonData)
                        return gameData
                    except:
                        return False

def selectDevice():
    print (u"Printing the device list:\n")
    ## The user didn't provide a packet source: Retrieve the local device list
    if (pcap_findalldevs(byref(alldevs), errbuf) == -1):
        print (u"Error in pcap_findalldevs: %s\n", errbuf.value)
        sys.exit(1)
    ## Print the list
    i=0
    d=alldevs.contents
    while d:
        i=i+1
        print (u"%d. %s" % (i, d.name))
        if (d.description):
            print (u" (%s)" % (d.description))
        else:
            print (u" (No description available)\n")
        if d.next:
            d=d.next.contents
        else:
            d=False
    if (i==0):
        print (u"\nNo interfaces found! Make sure WinPcap is installed.\n")
        sys.exit(-1)
    print (u"Enter the interface number (1-%d):" % (i))
    inum= raw_input(u'--> ')
    if inum in string.digits:
        inum=int(inum)
    else:
        inum=0
    if ((inum < 1) | (inum > i)):
        print (u"\nInterface number out of range.\n")
        ## Free the device list
        pcap_freealldevs(alldevs)
        sys.exit(-1)

    d=alldevs
    for i in range(0,inum-1):
        d=d.contents.next

    return d

def main():
    d = selectDevice()
    fp = pcap_open_live(d.contents.name,65536,1,10000,errbuf)
    if (fp == None):
        print (u"\nError opening adapter\n")
        ## Free the device list
        pcap_freealldevs(alldevs)
        sys.exit(-1)

    ## Read the packets
    res = pcap_next_ex( fp, byref(header), byref(pkt_data))
    while(res >= 0):
        if( win32api.GetKeyState(VK_ESCAPE)&0b10000000 ):
            print u"break"
            break
        if(res == 0):
            ## Timeout elapsed
            break

        gameData = packetToGameData( string_at(pkt_data, header.contents.len) )
        if( gameData ):
            try:
                pokerReadGameData.readGameData(gameData)
            except:
                print u"不明なパケット"
                print string_at(pkt_data, header.contents.len)
                print gameData

        res = pcap_next_ex( fp, byref(header), byref(pkt_data))

        if(res == -1):
            print (u"Error reading the packets: %s\n" % pcap_geterr(fp))
            sys.exit(-1)

    pcap_close(fp)
    sys.exit(0)

if __name__ == '__main__':
    main()