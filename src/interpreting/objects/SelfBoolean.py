from .SelfObject import *

class SelfBoolean(SelfObject):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def __str__(self):
		return f"SelfBoolean: (value='{self.value}')"

	def get_value(self):
		return self.value