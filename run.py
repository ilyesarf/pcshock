import os
import keyboard
from reader import *
from emit import *

ACTS = {"psbtn": ["exit"],
        "l1": ["ctrl", "shift", "tab"], 
        "r1": ["ctrl", "tab"], 
        "l2": ["alt", "ctrl", "left"],
        "r2": ["alt", "ctrl", "right"], 
        "l3": ["alt", "tab"], 
        "triangle": ["space"],
        "square": ["f"],
        "north": ["up"],
        "east": ["right"],
        "south": ["down"],
        "west": ["left"]}


def run_act(act):
    for key in act:
        if key == "exit":
            print("Program exited from controller")
            exit(1)
        keyboard.press(key)
    
    for key in act:
        keyboard.release(key)

if os.getenv('USB'):
    offset = 0
    reader = USB()
else:
    offset = 3
    reader = BT()

states = {key: [False, 0] for key in ACTS.keys()}
while True:

        emit(reader, red=123, blue=205, led_bright=1)
        try:
            buf = reader.read()[offset:]
            data = reader.parse(buf)
            for k in ACTS.keys():
                key = data[k]
                act = ACTS[k]
                state = states[k]
                st = time.monotonic()

                if key and not state[0]:
                    state[0] = True
                    state[1] = st

                elif not key and state[0]:
                    state[0] = False

                    if st - state[1] > 0.1:
                        run_act(act)
            
        except KeyboardInterrupt:
            exit(1)