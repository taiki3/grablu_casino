# -*- coding: utf-8 -*-
from ctypes import *
from winpcapy import *
from winpcapy_types import *
#import sys
import platform
import dpkt,socket
import json
import gzip
from StringIO import StringIO

class PacketDump():
    def __init__(self):
        if platform.python_version()[0] == "3":
            self.raw_input=input
        self.LINE_LEN=16
        self.alldevs=POINTER(pcap_if_t)()
        self.d=POINTER(pcap_if_t)
        self.fp=pcap_t
        self.errbuf= create_string_buffer(PCAP_ERRBUF_SIZE)
        self.header=POINTER(pcap_pkthdr)()
        self.pkt_data=POINTER(c_ubyte)()

    def selectDevice(self,iNum):
        d=self.alldevs
        for i in range(0,iNum-1):
            d=d.contents.next
        return d

    def getDeviceDict(self):
        if (pcap_findalldevs(byref(self.alldevs), self.errbuf) == -1):
            print (u"Error in pcap_findalldevs: %s\n", self.errbuf.value)
            sys.exit(1)

        i=0
        deviceDict = {}
        d=self.alldevs.contents
        while d:
            i=i+1
            deviceDict[i] = unicode(i)+u":"+d.description
            if d.next:
                d=d.next.contents
            else:
                d=False

        if (i==0):
            print (u"\nNo interfaces found! Make sure WinPcap is installed.\n")
            sys.exit(-1)

        return deviceDict

    def packetToGameData(self):
        packet = string_at(self.pkt_data, self.header.contents.len)
        eth = dpkt.ethernet.Ethernet(packet)
        if( type(eth.data) == dpkt.ip.IP ):
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            if( src==socket.gethostbyname(u'gbf.game.mbga.jp') ):
                if( type(ip.data) == dpkt.tcp.TCP ):
                    tcp = ip.data
                    if( tcp.sport == 80 and len(tcp.data)>0 ):
                        index = tcp.data.find('Content-Length: ')
                        if( index>0 ):
                            cLength = ""
                            i = len('Content-Length: ')
                            while tcp.data[index+i]!= chr(13):
                                cLength+=tcp.data[index+i]
                                i+=1

                            headerLength = tcp.data.find('\r\n\r\n') + len('\r\n\r\n')

                            while len(tcp.data)-headerLength < int(cLength) :
                                self.getPacket()
                                pPacket = string_at(self.pkt_data, self.header.contents.len)
                                pEth = dpkt.ethernet.Ethernet(pPacket)
                                pIp = pEth.data
                                pTcp = pIp.data
                                tcp.data+=pTcp.data

                        try:
                            http = dpkt.http.Response(tcp.data)
                            if( http.headers[u'content-type'] == u'application/json' ):
                                jsonData = gzip.GzipFile( fileobj=StringIO(http.body) ).read()
                                if( u"{" in jsonData ):
                                    gameData = json.loads(jsonData)
                                    return gameData

                            else:
                                return False

                        except:
                            return False

        return False

    def getPacket(self):
        return pcap_next_ex( self.fp, byref(self.header), byref(self.pkt_data))

    def runPacketDump(self,device):
        self.fp = pcap_open_live(device.contents.name,65536,False,8000,self.errbuf)
        bPro = bpf_program()
        filterExp = u"tcpdump src host gbf.game.mbga.jp"
        pFilterExp = STRING(filterExp)
        pcap_compile(self.fp,bPro,pFilterExp,0,0)
        pcap_setfilter(self.fp,bPro)
        if (self.fp == None):
            print (u"\nError opening adapter\n")
            ## Free the device list
            pcap_freealldevs(self.alldevs)
            sys.exit(-1)

    def closePacketDump(self):
        pcap_close(self.fp)

if __name__ == '__main__':
    pass
    #myclass = PacketDump()
    #myclass.getDeviceDict()