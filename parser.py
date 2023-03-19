
from hexdump import hexdump
import usb.core
import usb.util
import os

DEBUG = os.getenv('DEBUG')

DEV_TO_HOST = usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE)

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

    def detach(self, id=0):
        if self.dev.is_kernel_driver_active(id):
            self.dev.detach_kernel_driver(id)
            print(f"Interface number {id} detached from kernel")
    
    def read(self, report_id, size):
        data = self.dev.ctrl_transfer(DEV_TO_HOST, 0x01, report_id, 0, size+1)[1:].tobytes()

        return data

if DEBUG:
    reader = Reader(idv=0x275d, idp=0x0ba6) #mouse test
else:
    reader = Reader()

"""
buf = reader.read(0x12, 6+3+6)
ds4_mac, unk, host_mac = buf[0:6], buf[6:9], buf[9:15]

print(ds4_mac, host_mac)
"""
