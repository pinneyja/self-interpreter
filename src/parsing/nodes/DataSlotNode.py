from interpreting.objects.Slot import *

class DataSlotNode:
	def __init__(self, name, operator = None, expression = None):
		self.name = name
		self.operator = operator
		self.expression = expression

	def __str__(self):
		return "DataSlot: name='{}' operator='{}' expression='{}'".format(self.name, self.operator, self.expression)

	def interpret(self, environment):
		if (not self.expression):
			return Slot(self.name)
		else:
			return Slot(self.name, self.expression.interpret(environment), self.operator == "=")