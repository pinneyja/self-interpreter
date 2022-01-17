from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.primitive_objects.SelfByteVector import SelfByteVector

class SelfString(SelfObject):
	def __init__(self, value, slots = None):
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.value = value
		self.byte_vector = SelfByteVector(value)

	def __str__(self):
		return f"SelfString: (value='{self.value}', byte_vector={self.byte_vector})"

	def as_dict(self, visited):
		dict = super().as_dict(visited)
		dict['annotation'] = self.value
		dict['alt_string'] = True
		return dict