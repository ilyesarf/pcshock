

class Parser:
    def __init__(self, buf):
        self.buf = buf
        self.presses = {}
    
    def get_press(self):
        return self.presses

    def get_buttons(self):
        data = self.buf[5]
        buttons = dict.fromkeys(['square', 'cross', 'circle', 'triangle'], False)

        bits = [2**i for i in range(4, 8)] 
        for btn, bit in zip(buttons.keys(), bits):
            buttons[btn] = (data&bit)!=0

        return buttons
