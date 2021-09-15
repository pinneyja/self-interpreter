class DataSlotNode:
	def __init__(self, name, operator = None, expression = None):
		self.name = name
		self.operator = operator
		self.expression = expression

	def __str__(self):
		return "DataSlot: name='{}' operator='{}' expression='{}'".format(self.name, self.operator, self.expression)
