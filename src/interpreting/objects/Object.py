
class Object:
	def __init__(self, slots = {}):
		self.slots = slots

	def __str__(self):
		output  = "Object:{"
		for key in self.slots:
			output += "{},".format(self.slots[key])
		return output + "}"