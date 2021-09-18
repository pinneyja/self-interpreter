from interpreting.objects.IntObject import IntObject

class IntegerNode:
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return "Integer: {}".format(self.value)

	def interpret(self, environment):
		return IntObject(self.value)