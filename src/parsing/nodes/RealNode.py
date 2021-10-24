from interpreting.objects.SelfReal import SelfReal
from .Node import Node
import re

class RealNode(Node):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def __str__(self):
		return "Real: ('{}')".format(self.value)

	def interpret(self, context):
		return SelfReal(self.value)
	
	def verify_syntax(self):
		self.value = float(self.value)