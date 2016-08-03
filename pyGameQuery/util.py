def printsafe(data):
    result = ""
    for i in data:
        if 0x20 <= i <= 0x7E:
            result = result + chr(i)
        else:
            result = result + "."
    return result

def hexdump(data):
    info = ""
    l = len(data)
    for i in range(0, l, 0x10):
        hexdump = ""
        for x in range(i, i+0x8 if i+0x8 <= l else l):
            hexdump = hexdump + "{0:02X} ".format(data[x])
        hexdump = hexdump + " "
        for x in range(i+0x8, i+0x10 if i+0x10 <= l else l):
            hexdump = hexdump + "{0:02X} ".format(data[x])
        info = info + "{0:04X}     {1: <49s}     {2:s}\n".format(i, hexdump, printsafe(data[i:i+0x10]))
    return info
