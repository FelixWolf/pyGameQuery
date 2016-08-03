#SourceQuery generic exceptions
class sourceQueryCRC32(Exception):
    def __init__(self,expected,got):
        Exception.__init__(self,"Expected {0:08x}, got {0:08x}!".format(
            expected, got
        ))
        self.expected = expected
        self.got = got
        
class sourceQuerySize(Exception):
    def __init__(self,expected,got):
        Exception.__init__(self,"Expected {0} bytes, got {0} bytes!".format(
            expected, got
        ))
        self.expected = expected
        self.got = got
        
#SourceQuery Info
class sourceQueryInfoType(Exception):
    def __init__(self,expected,got):
        Exception.__init__(self,"Expected 0x{0:02x}}, got 0x{0:02x}}!".format(
            expected, got
        ))
        self.expected = expected
        self.got = got
