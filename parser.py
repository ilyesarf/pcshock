

import usb.core
import usb.util
import bluetooth
import os
import time
import socket
from errors import *

DEBUG = os.getenv('DEBUG')

class USB:
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
        data = self.ep.read(size, timeout=50) 
        
        return data

class BT:
    def __init__(self, name="Wireless Controller"):
        self.name = name
        self.ds4_addr = self.find_ds4()
        self.sock = self.connect_ds4()


    def find_ds4(self):
        print("Discovering devices")
        devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
        if len(devices) == 0:
            raise DiscoveryError("No bluetooth device has been detected")

        ds4_addr = None
        for addr, name in devices:
            if name == self.name:
                ds4_addr = addr
                print(f"Controller found (address: {ds4_addr})")
                break
        
        if not ds4_addr:
            raise DS4BTError("DualShock4 device has not been detected")

        return ds4_addr

    def connect_ds4(self):
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET,socket.BTPROTO_L2CAP)
        print(self.ds4_addr)
        sock.connect((self.ds4_addr, 0x13))

        return sock
    
    def read(self, size=0x40):
        data = self.sock.recv(size)

        return data

if __name__ == '__main__':
    if DEBUG:
        reader = Reader(idv=0x275d, idp=0x0ba6) #mouse test
        print(reader.read(100))
    else:
        if os.getenv('USB'):
            reader = USB()
            buf = reader.read()
        else:
            reader = BT()
            buf = reader.read()[2:]

        print(buf[5])
        print(buf[2])
        
