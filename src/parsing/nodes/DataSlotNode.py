from interpreting.objects.SelfSlot import *
from .Node import Node

class DataSlotNode(Node):
	def __init__(self, name, operator = None, expression = None):
		super().__init__()
		self.name = name
		self.operator = operator
		self.expression = expression

	def __str__(self):
		return "DataSlot: (name='{}' operator='{}' expression='{}')".format(self.name, self.operator, self.expression)

	def interpret(self, context):
		if (not self.expression):
			return SelfSlot(self.name)
		else:
			return SelfSlot(self.name, self.expression.interpret(context), self.operator == "=")