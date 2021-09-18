class SelfObject:
	def __init__(self, slots = {}):
		self.slots = slots

	def __str__(self):
		output  = "SelfObject:{"
		for key in self.slots:
			output += "{},".format(self.slots[key])
		return output + "}"