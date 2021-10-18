from typing import OrderedDict
from .SelfObject import *
from interpreting.objects.SelfByteVector import *

class SelfString(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.value = value
		self.byte_vector = SelfByteVector(value)

	def __str__(self):
		return f"SelfString: (value='{self.value}', byte_vector={self.byte_vector})"