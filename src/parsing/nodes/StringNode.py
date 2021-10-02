from interpreting.objects.SelfString import *

class StringNode:
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return "String: ('{}')".format(self.value)

	def interpret(self, context):
		return SelfString(self.value)