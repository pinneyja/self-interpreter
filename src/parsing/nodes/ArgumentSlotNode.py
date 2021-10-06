from interpreting.objects.SelfSlot import *
from .Node import Node

class ArgumentSlotNode(Node):

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "ArgumentSlot: (name='{}')".format(self.name)

	def interpret(self, context):
		return SelfSlot(self.name)