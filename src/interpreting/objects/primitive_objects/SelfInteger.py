from interpreting.objects.traits.SelfSmallInt import SelfSmallInt
from Messages import Messages
import warnings

class SelfInteger(SelfSmallInt):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.value = value
		if (type(value) is not int):
			warnings.warn(Messages.NUMBER_NOT_VERIFIED.value.format('integer', self.value))
			self.value = int(value)

	def __str__(self):
		return f"SelfInteger: (value='{self.value}')"

	def __hash__(self):
		return hash(self.value)

	def get_value(self):
		return self.value