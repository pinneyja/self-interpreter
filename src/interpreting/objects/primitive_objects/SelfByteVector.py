from interpreting.objects.primitive_objects.SelfObjectVector import SelfObjectVector

class SelfByteVector(SelfObjectVector):
	def __init__(self, value, slots = None):
		from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
		super().__init__()

		if slots:
			self.slots.update(slots)

		self.indexable = list(map(SelfInteger, map(ord, value)))

	def __str__(self):
		return "SelfByteVector: {}".format(list(map(str, self.indexable)))

	def as_dict(self, visited):
		dict = super().as_dict(visited)
		dict['annotation'] = list(map(lambda x : x.get_value(), self.indexable))
		dict['alt_string'] = True
		return dict