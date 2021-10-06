from typing import OrderedDict
from .SelfObject import *

class SelfByteVector(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__(slots)
		
		if slots is None:
			slots = OrderedDict()

		self.value = list(map(ord, value))

	def __str__(self):
		return "SelfByteVector: {}".format(self.value)