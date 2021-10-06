from interpreting.objects.SelfInteger import SelfInteger
from .Node import Node

class IntegerNode(Node):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def __str__(self):
		return "Integer: ('{}')".format(self.value)

	def interpret(self, context):
		return SelfInteger(self.value)