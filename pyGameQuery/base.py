import socket
import struct

class serverQuery:
    sock = None
    packetSize = 1400
    payload = b""
    host = ("", 0)
    def __init__(self, ip, port, timeout = 1):
        """DON'T TOUCH ME"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", 0))
        self.host = (ip, port)
        self.sock.settimeout(timeout)
        self.sendRequest()
        
    def recv(self):
        """Internal function for receiving packets"""
        while True:
            try:
                data, addr = self.sock.recvfrom(self.packetSize)
            except socket.timeout:
                break
                
            if not data:
                break
                
            try:
                if self.processData(data):
                    self.sock.close()
                    break
            except Exception as e:
                self.sock.close()
                raise e
        
        self.processResponse()
        return self.payload
    
    def send(self, data):
        try:
            self.sock.sendto(data, self.host)
            return True
        except OSError:
            return False
    
    def processData(self, data):
        """Called each time new data is received
            return true to break(AKA: Response end)
            return false to continue(AKA: Still need data)"""
        self.payload = self.payload + data
        return False
    
    def sendRequest(self):
        """Sent to server to initialize request"""
        pass
    
    def processResponse(self):
        """Called before return payload"""
        pass
