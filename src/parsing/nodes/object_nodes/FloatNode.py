from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
from parsing.nodes.Node import Node

class FloatNode(Node):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def __str__(self):
		return "Real: ('{}')".format(self.value)

	def interpret(self, context):
		return SelfFloat(self.value)
	
	def verify_syntax(self):
		self.value = float(self.value)