
from hexdump import hexdump
import usb.core
import usb.util
import os

DEBUG = os.getenv('DEBUG')

class Reader:
    def __init__(self, idv=0x054c, idp=0x09cc):
        self.dev = usb.core.find(idVendor=idv, idProduct=idp)
        if not self.dev:
            raise ConnectionError("Can't connect to device")
        print(f"Connected to device (VendorID: {idv}, ProductID: {idp})")

        self.dev.reset()
        if idv == 0x054c and idp == 0x09cc: #for controller
            self.intf = 3
            for i in range(self.intf+1):
                self.detach(i)
        else:
            self.intf = 0
            self.detach()

        self.dev.set_configuration()
        self.ep = self.get_ep()
    
    def detach(self, id=0):
        if self.dev.is_kernel_driver_active(id):
            self.dev.detach_kernel_driver(id)
            print(f"Interface number {id} detached from kernel")
    
    def get_ep(self): 
        ep = self.dev[0][(self.intf,0)][0]

        return ep
    
    def read(self, size=0x40):
        #eaddr = self.ep.bEndpointAddress
        data = self.ep.read(size) 
        
        return data

if DEBUG:
    reader = Reader(idv=0x275d, idp=0x0ba6) #mouse test
    print(reader.read(100))
else:
    reader = Reader()
    print(reader.read()[8]) #L2

