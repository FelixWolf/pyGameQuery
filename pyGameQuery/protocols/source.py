import struct
import bz2
from binascii import crc32

from ..exceptions.source import sourceQueryCRC32
from ..exceptions.source import sourceQuerySize

from ..exceptions.source import sourceQueryInfoType

from .. import base
from .. import util

#Constraints
SERVER_TYPE_DEDICATED = 0
SERVER_TYPE_LISTEN = 1
SERVER_TYPE_SOURCETV = 2

SERVER_OS_LINUX = 0
SERVER_OS_WINDOWS = 1
SERVER_OS_MAC = 2

SERVER_VISIBILITY_PUBLIC = 0
SERVER_VISIBILITY_PRIVATE = 1

SERVER_VAC_UNSECURE = 0
SERVER_VAC_SECURE = 1

#Source string reader:
def unpackString(src, offset = 0):
    res = []
    while True:
        if src[offset] == 0:
            break
        res.append(src[offset])
        offset = offset + 1
    return bytes(res).decode()

class sourceQueryBase(base.serverQuery):
    multi = {
        "compressed": False,
        "size": 0,
        "crc32": 0,
        "count": 0,
        "recv": {}
    }
    def processData(self, data):
        """Called each time new data is received
            return true to break(AKA: Response end)
            return false to continue(AKA: Still need data)"""
        header = struct.unpack_from("<l", data)[0]
        data = data[4:]
        if header == -1:
            #Simple response
            self.payload = self.payload + data
        elif header == -2:
            #Multi-response
            ID, total, number, size = struct.unpack_from("<lBBh", data)
            if number == 0:
                #Compression?
                if ID&0x8000000:
                    self.multi["size"], self.multi["crc32"] = \
                        struct.unpack_from("<ll", data, 12)
                    self.multi["recv"][number] = data[32:]
                    self.multi["compressed"] = True
                else:
                    self.multi["recv"][number] = data[12:]
            else:
                self.multi["recv"][number] = data[12:]
            
            self.multi["count"] = self.multi["count"] + 1
            #We could do number == total, but we get packets out of order!
            if self.multi["count"] == total:
                for i in range(total):
                    self.payload = self.payload + self.multi["recv"][i]
                if self.multi["compressed"]:
                    self.payload = bz2.decompress(self.payload)
                    if len(self.payload) != self.multi["size"]:
                        raise sourceQuerySize(
                            self.multi["size"],
                            len(self.payload)
                        )
                    h = crc32(self.payload)
                    if h != self.multi["crc32"]:
                        raise sourceQueryCRC32(
                            self.multi["crc32"],
                            h
                        )
                return True
        return False

#<Source Query>
#Type      |T| Info
#----------+-+------------------------------------------------------------------
#byte      |B| 8 bit character or unsigned integer
#short     |h| 16 bit signed integer
#long      |l| 32 bit signed integer
#float     |f| 32 bit floating point
#long long |q| 64 bit unsigned integer
#string	   |?| variable-length byte field, encoded in UTF-8, terminated by 0x00


class sourceQueryInfo(sourceQueryBase):
    def sendRequest(self):
        self.send(b"\xFF\xFF\xFF\xFF\x54Source Engine Query\x00")
        
    def get(self):
        pl = self.recv()
        res = {}
        head, res["Protocol"] = struct.unpack_from("<BB", pl)
        offset = 2
        if head != 0x49:
            raise sourceQueryInfoType(0x49, head)
            
        res["Name"] = unpackString(pl, offset)
        offset = offset + len(res["Name"]) + 1
        
        res["Map"] = unpackString(pl, offset)
        offset = offset + len(res["Map"]) + 1
        
        res["Folder"] = unpackString(pl, offset)
        offset = offset + len(res["Folder"]) + 1
        
        res["Game"] = unpackString(pl, offset)
        offset = offset + len(res["Game"]) + 1
        
        res["ID"], res["Players"], res["Max_Players"], res["Bots"], \
            res["Server_Type"], res["Environment"], res["Visibility"], \
            res["VAC"] = struct.unpack_from("<hBBBBBBB", pl, offset)
        offset = offset + 9
        
        #Fix for "cannot follow standards: the game" AKA: The Ship
        if res["ID"] == 2400:
            res["TheShip_Mode"], res["TheShip_Witnesses"], res["Duration"] \
                = struct.unpack_from("<BBB", pl, offset)
            offset = offset + 3
            
        res["Version"] = unpackString(pl, offset)
        offset = offset + len(res["Version"]) + 1
        
        res["EDF"], = struct.unpack_from("<B", pl, offset)
        offset = offset + 1
        
        if res["EDF"]&0x80:
            res["Port"], = struct.unpack_from("<h", pl, offset)
            offset = offset + 2
        else:
            res["Port"] = self.host[1]
            
        if res["EDF"]&0x10:
            res["SteamID"], = struct.unpack_from("<q", pl, offset)
            offset = offset + 8
        else:
            res["SteamID"] = None
            
        if res["EDF"]&0x40:
            res["SourceTV_Port"], = struct.unpack_from("<h", pl, offset)
            offset = offset + 2
            res["SourceTV_Name"] = unpackString(pl, offset)
            offset = offset + len(res["SourceTV_Host"]) + 1
        else:
            res["SourceTV_Port"] = None
            res["SourceTV_Name"] = ""
            
        if res["EDF"]&0x20:
            res["Keywords"] = unpackString(pl, offset)
            offset = offset + len(res["Keywords"]) + 1
        else:
            res["Keywords"] = ""
            
        if res["EDF"]&0x01:
            res["GameID"], = struct.unpack_from("<q", pl, offset)
            offset = offset + 8
        else:
            res["GameID"] = None
            
        print(util.hexdump(pl))
        return res
        
        
