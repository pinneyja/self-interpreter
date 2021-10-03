import copy

class SelfSlot:
	def __init__(self, name, value=None, isImmutable=False):
		self.name = name
		self.value = value
		self.isImmutable = isImmutable

	def __str__(self):
		return "SelfSlot:{{name='{}', value={{{}}}, isImmutable='{}'}}".format(
			self.name, self.value, self.isImmutable
		)

	def get_value(self, arg=None):
		if self.value.code:
			clone = copy.deepcopy(self.value)
			for key in clone.arg_slots:
				clone.slots[key] = SelfSlot(key, arg)
			return self.value.code.interpret(clone)
		else:
			return self.value