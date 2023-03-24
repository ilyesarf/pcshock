import inspect

class Parser:	
	def parse(self, buf):
		presses = {}
		functions = [func[1] for func in inspect.getmembers(self, predicate=inspect.ismethod) if func[0].startswith('get_')]
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

