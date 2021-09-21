class SelfException():
	def __init__(self, message):
		self.message = message
	
	def __str__(self):
		return "SelfException: (message='{}')".format(self.message)