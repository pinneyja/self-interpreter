from .SelfObject import *

class SelfInteger(SelfObject):
	def __init__(self, value, slots = {}):
		super().__init__(slots)
		self.value = value

	def __str__(self):
		return "SelfInteger: (value='{}')".format(self.value)