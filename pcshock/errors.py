
class ConnectionError(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

class DiscoveryError(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

class DS4BTError(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message) 
