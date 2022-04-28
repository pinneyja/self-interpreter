import warnings
from interpreting.objects.SelfSlot import SelfSlot
from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.primitive_objects.SelfLobby import SelfLobby
from interpreting.objects.SelfException import SelfException
from Messages import Messages

class SelfInteger(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.value = value
		self.name = str(self.get_value())
		if (type(value) is not int):
			warnings.warn(Messages.NUMBER_NOT_VERIFIED.value.format('integer', self.value))
			self.value = int(value)

		try:
			traits_smallInt = SelfLobby.get_lobby().slots["traits"].value.pass_unary_message("smallInt")
			self.parent_slots["parent"] = SelfSlot("parent", traits_smallInt)
		except SelfException as e:
			pass

	def __str__(self):
		return f"SelfInteger: (value='{self.value}')"

	def __hash__(self):
		return hash(self.value)

	def get_value(self):
		return self.value

	def as_dict(self, visited):
		dict = super().as_dict(visited)
		dict['annotation'] = self.value
		dict['alt_string'] = True
		return dict