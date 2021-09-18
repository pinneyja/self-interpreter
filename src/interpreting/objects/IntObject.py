from .Object import *

class IntObject(Object):
	def __init__(self, value, slots = {}):
		super().__init__(slots)
		self.value = value

	def __str__(self):
		return "IntObject: (value='{}')".format(self.value)