from reader import *
from emit import emit
import time, os

if not os.getenv('USB'):
    offset = 3
    reader = BT()
else:
    offset = 0
    reader = USB()

KEYS = ['psbtn', 'cross']
modes = [(150, 100, 0, 255, 0, 100, 0), (175, 150, 200, 165, 0, 100, 0), (255, 255, 255, 0, 0, 100, 0)]
states = {key: [False, 0] for key in KEYS}
mode = 0

emit(reader, 50, 50, 100, 0, 203, 100, 0)
time.sleep(1)
while True:
    try:
        buf = reader.read()[offset:]
        data = reader.parse(buf)

        for key in KEYS:
            state = states[key]
            val = data[key]

            st = time.monotonic()

            if val and not state[0]:
                state[0] = True
                state[1] = st

            elif not val and state[0]:
                state[0] = False
                if key == 'cross':
                    if st - state[1] > 0.1:
                        mode += 1
                        if mode == 3:
                            mode = 0
                elif key == 'psbtn':
                    emit(reader)
                    exit(1)

        emit(reader,*modes[mode])
    except KeyboardInterrupt:
        emit(reader)
        exit(1)