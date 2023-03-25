import inspect

class Parser:   
    @classmethod
    def parse(cls, buf):
        presses = {}
        functions = [func[1] for func in inspect.getmembers(cls, predicate=inspect.ismethod) if func[0].startswith('get_')]
        for func in functions:
            presses.update(func(buf))
        
        return presses

    @classmethod
    def get_buttons(cls, buf):
        data = buf[5]
        buttons = dict.fromkeys(['square', 'cross', 'circle', 'triangle'], False)

        bits = [2**i for i in range(4, 8)] 
        for btn, bit in zip(buttons.keys(), bits):
            buttons[btn] = (data&bit)!=0

        return buttons
    
    @classmethod
    def get_battery(cls, buf):
        btt = {'battery': buf[30]%16}

        return btt
