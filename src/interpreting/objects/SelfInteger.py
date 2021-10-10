from .SelfSmallInt import *

class SelfInteger(SelfSmallInt):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots is not None:
			self.slots.update(slots)

		self.value = value

	def __str__(self):
		return f"SelfInteger: (value='{self.value}')"

	def get_value(self):
		return self.value