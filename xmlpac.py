def xmlToPacket(filen):
    tree = ET.parse(filen)
    pacs = [u for u in tree.findall("packet")]
    return pacs

def packetToProto(pacs):
    protos = [proto for protos in pacs for proto in protos.findall("proto") if proto.get("name")=="media"]
    return protos

def protosToField(protos):
    fields = [field.find("field") for field in protos ]
    return fields

def fieldToValue(fields):
    values = [b2a.unhexlify(field.get("value")) for field in fields]
    return values

def decodeValue(values):
    decoded = [json.loads(deco.decode('utf-8')) for deco in values]
    return decoded    tree = Et.Parse(filen)
    pacs = [u for u in tree tree.findall("packet")]
    return pacs
