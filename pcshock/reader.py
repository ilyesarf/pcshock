

import usb.core
import usb.util
import bluetooth
import os
import socket
from pcshock.errors import *
from pcshock.parser import Parser


DEBUG = os.getenv('DEBUG')

class USB(Parser):
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
        self.in_ep = self.dev[0][(self.intf,0)][0]
        self.out_ep = self.dev[0][(self.intf, 0)][1]

    def detach(self, id=0):
        if self.dev.is_kernel_driver_active(id):
            self.dev.detach_kernel_driver(id)
            print(f"Interface number {id} detached from kernel")
    
    def read(self, size=0x40):
        data = self.in_ep.read(size, timeout=50) 
        
        return data 
    
    def write(self, data):
        self.out_ep.write(data)

class BT(Parser):
    def __init__(self, name="Wireless Controller"):
        self.name = name
        if not os.path.exists('ds4_addr'):
            self.ds4_addr = self.find_ds4()
            self.save_ds4_addr(self.ds4_addr)
        else:
            self.ds4_addr = self.read_ds4_addr()
        
        self.send_sock = self.init_report()
        self.recv_sock = self.connect_ds4()

    def save_ds4_addr(self, ds4_addr): open('ds4_addr', 'w').write(ds4_addr)
    def read_ds4_addr(self): return open('ds4_addr', 'r').read()

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
    
    def init_report(self): #to get full report
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET,socket.BTPROTO_L2CAP)
        sock.connect((self.ds4_addr, 0x11))
        enable_report = b'\x43\x02'
        sock.send(enable_report)

        return sock
    
    def connect_ds4(self):
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET,socket.BTPROTO_L2CAP)
        sock.connect((self.ds4_addr, 0x13))

        return sock 
    
    def read(self, size=0x40):
        data = self.recv_sock.recv(size)
        return data

    def write(self, data):
        self.send_sock.send(data)

