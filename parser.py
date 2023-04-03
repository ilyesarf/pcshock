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
        buttons = {key: False for key in ['square', 'cross', 'circle', 'triangle']}

        bits = [2**i for i in range(4, 8)] 
        for btn, bit in zip(buttons.keys(), bits):
            buttons[btn] = (data&bit)!=0

        return buttons

    @classmethod
    def get_hats(cls, buf):
        arrang = {'0': ['north'], '1': ['north', 'east'], '2': ['east'], '3': ['south', 'east'], '4': ['south'], '5': ['south', 'west'], '6': ['west'], '7': ['north','west']}

        data = buf[5]
        hats = {key: False for key in ['north', 'east', 'south', 'west']}

        hat = data&15
        if hat != 8:
            for h in arrang[str(hat)]:
                hats[h] = True
        
        return hats

    
    @classmethod
    def get_battery(cls, buf):
        btt = {'battery': buf[30]%16}

        return btt

    @classmethod
    def get_analogs(cls, buf):
        data = buf[6]
        analogs = {key: False for key in ['l1', 'r1', 'l2', 'r2', 'share', 'opt', 'l3', 'r3']}

        bits = [2**i for i in range(8)] 
        for anl, bit in zip(analogs.keys(), bits):
            analogs[anl] = (data&bit)!=0

        return analogs
    
    @classmethod
    def get_psbtn(cls, buf):
        data = {'psbtn': (buf[7]&1)!=0}

        return data