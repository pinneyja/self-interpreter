from typing import OrderedDict
from .SelfObject import *

class SelfInteger(SelfObject):
	def __init__(self, value, slots = OrderedDict()):
		super().__init__(slots)
		self.value = value

	def __str__(self):
		return "SelfInteger: (value='{}')".format(self.value)