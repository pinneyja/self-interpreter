from typing import OrderedDict
from .SelfObject import *

class SelfInteger(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__(slots)		
		
		if slots is None:
			slots = OrderedDict()

		self.value = value

	def __str__(self):
		return "SelfInteger: (value='{}')".format(self.value)