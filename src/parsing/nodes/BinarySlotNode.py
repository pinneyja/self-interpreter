from interpreting.objects.SelfSlot import *

class BinarySlotNode:
	def __init__(self, name, expression, arg_name = None):
		self.name = name
		self.expression = expression
		self.arg_name = arg_name

	def __str__(self):
		return "BinarySlot: (name='{}' expression='{}' arg_name='{}')".format(self.name, self.expression, self.arg_name)

	def interpret(self, context):
		return SelfSlot(self.name, self.expression.interpret(context), True)