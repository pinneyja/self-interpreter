class SelfSlot:
	def __init__(self, name, value=None, isImmutable=False):
		self.name = name
		self.value = value
		self.isImmutable = isImmutable

	def __str__(self):
		return "SelfSlot:{{name='{}', value={{{}}}, isImmutable='{}'}}".format(
			self.name, self.value, self.isImmutable
		)

	def get_value(self):
		if self.value.code:
			return self.value.code.interpret()
		else:
			return self.value