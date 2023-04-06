import os
try:
    import pyautogui 
except:
    os.system('xhost +')
    import pyautogui
import keyboard
import time
from reader import *
from emit import *

ACTS = {'psbtn': ['exit'], 
        'l1': ['keyb', 'ctrl', 'shift', 'tab'], 
        'r1': ['keyb', 'ctrl', 'tab'], 
        'l2': ['keyb', 'alt', 'ctrl', 'left'], 
        'r2': ['keyb', 'alt', 'ctrl', 'right'], 
        'l3': ['keyb', 'alt', 'tab'], 
        'cross': ['click', 'left'],
        'triangle': ['keyb', 'space'], 
        'square': ['keyb', 'f'], 
        'north': ['keyb', 'up'], 
        'east': ['keyb', 'right'], 
        'south': ['keyb', 'down'], 
        'west': ['keyb', 'left']}



def run_act(act, reader):
    if act[0] == "keyb":
        keys = act[1:]
        for key in keys:
            keyboard.press(key)
        
        for key in keys:
            keyboard.release(key)

    elif act[0] == "exit":
        print("Program exited from controller")
        emit(reader)
        exit(1)
    
    elif act[0] == "click":
        click = act[1]
        pyautogui.click(button=click)

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
                        run_act(act, reader)
            
        except KeyboardInterrupt:
            emit(reader)
            exit(1)