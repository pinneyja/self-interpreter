from interpreting.objects.SelfSlot import *
from parsing.nodes.ArgumentSlotNode import *
from .Node import Node
from parsing.SelfParsingError import *
from parsing.nodes.ArgumentSlotNode import *

class BinarySlotNode(Node):
	def __init__(self, name, expression, arg_name = None):
		super().__init__()
		self.name = name
		if arg_name:
			expression.slot_list.append(ArgumentSlotNode(arg_name))
		self.expression = expression

	def __str__(self):
		return "BinarySlot: (name='{}' expression='{}')".format(self.name, self.expression)

	def interpret(self, context):
		return SelfSlot(self.name, self.expression.interpret(context), True)
	
	def verify_syntax(self):
		self.expression.set_allowable_argument_slot_count(1)
		self.expression.verify_syntax()