from pcshock.reader import *
from pcshock.emit import emit
import time, os

if not os.getenv('USB'):
    offset = 3
    reader = BT()
else:
    offset = 0
    reader = USB()

keys = ['cross', 'psbtn']
modes = [(150, 100, 0, 255, 0, 100, 0), (175, 150, 200, 165, 0, 100, 0), (255, 255, 255, 0, 0, 100, 0)]
states = {k: [False, 0] for k in keys}
mode = 0

emit(reader, 50, 50, 100, 0, 203, 100, 0)
time.sleep(1)
while True:
    try:
        buf = reader.read()[offset:]
        data = reader.parse(buf)
        for k in keys:
            state = states[k]
            key = data[k]
            st = time.monotonic()

            if key and not state[0]:
                state[0] = True
                state[1] = st

            elif not key and state[0]:
                state[0] = False

                if st - state[1] > 0.1:
                    if k == 'cross':
                        mode += 1
                        if mode == 3:
                            mode = 0
                    elif k == 'psbtn':
                        print('Program exited from controller')
                        emit(reader)
                        exit(1)

        emit(reader,*modes[mode])
    except KeyboardInterrupt:
        emit(reader)
        exit(1)