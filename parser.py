import inspect

class Parser:   
    @classmethod
    def parse(cls, buf, acts: dict):
        presses = {}
        functions = [func[1] for func in inspect.getmembers(cls, predicate=inspect.ismethod) if func[0].startswith('get_')]
        for func in functions:
            presses.update(func(buf))
        
        for key in acts.keys():
            v = presses[key] 
            presses[key] = v + [acts[key]]
            
        return presses

    @classmethod
    def get_buttons(cls, buf):
        data = buf[5]
        buttons = {key: list([False]) for key in ['square', 'cross', 'circle', 'triangle']}

        bits = [2**i for i in range(4, 8)] 
        for btn, bit in zip(buttons.keys(), bits):
            buttons[btn][0], = [(data&bit)!=0]

        return buttons
    
    @classmethod
    def get_battery(cls, buf):
        btt = {'battery': buf[30]%16}

        return btt

    @classmethod
    def get_analogs(cls, buf):
        data = buf[6]
        analogs = {key: list([False]) for key in ['l1', 'r1', 'l2', 'r2', 'share', 'opt', 'l3', 'r3']}

        bits = [2**i for i in range(8)] 
        for anl, bit in zip(analogs.keys(), bits):
            analogs[anl][0] = (data&bit)!=0

        return analogs
