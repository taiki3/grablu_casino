import binascii as b2a
import xml.etree.ElementTree as ET
import os
import sys
import xmlpac as xpc

def main():
    pacs = xpc.xmlToPacket("..\FILENAME.xml")
    protos = xpc.packetToProto(pacs)
    fields = xpc.protosToField(protos)
    values = xpc.fieldToValue(fields)
    decoded = xpc.decodeValue(values)
    print(decoded)

if __name__ == '__main__':
    main()
