from Messages import Messages
from interpreting.objects.SelfSlot import SelfSlot
from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.primitive_objects.SelfLobby import SelfLobby
from interpreting.objects.SelfException import SelfException
import warnings

class SelfFloat(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.value = value
		if (type(value) is not float):
			warnings.warn(Messages.NUMBER_NOT_VERIFIED.value.format('float', self.value))
			self.value = float(value)

		try:
			traits_float = SelfLobby.get_lobby().slots["traits"].value.pass_unary_message("float")
			self.parent_slots["parent"] = SelfSlot("parent", traits_float)
		except SelfException as e:
			pass

	def __str__(self):
		return f"SelfFloat: (value='{self.value}')"

	def __hash__(self):
		return hash(self.value)

	def get_value(self):
		return self.value

	def as_dict(self, visited):
		dict = super().as_dict(visited)
		dict['annotation'] = self.value
		dict['alt_string'] = True
		return dict