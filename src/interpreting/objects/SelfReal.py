from .SelfSmallInt import *

class SelfReal(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.value = value

	def __str__(self):
		return f"SelfReal: (value='{self.value}')"

	def get_value(self):
		return self.value