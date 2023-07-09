
from pcshock.reader import *

def emit(reader, rumble1=0, rumble2=0, red=0, green=0, blue=0, led_bright=0, led_dim=0):
    if isinstance(reader, BT):
        offset = 2
        pkt = bytearray(79)
        pkt[0] = 0x52
        pkt[1] = 0x11
        pkt[2] = 0x80
        pkt[4] = 0xff
    elif isinstance(reader, USB):
        offset = -1
        pkt = bytearray(32)
        pkt[0] = 0x05
        pkt[1] = 0xff


    data = [rumble1, rumble2, red, green, blue, led_bright, led_dim]
    for i, v in enumerate(data):
        pkt[offset+i+5] = min(v, 255)

    reader.write(pkt)


