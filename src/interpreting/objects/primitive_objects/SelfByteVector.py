from typing import OrderedDict
from interpreting.objects.SelfObject import SelfObject

class SelfByteVector(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.value = list(map(ord, value))

	def __str__(self):
		return "SelfByteVector: {}".format(self.value)