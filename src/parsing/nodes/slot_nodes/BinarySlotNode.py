from interpreting.objects.SelfSlot import SelfSlot
from parsing.nodes.Node import Node
from parsing.nodes.slot_nodes.ArgumentSlotNode import ArgumentSlotNode

class BinarySlotNode(Node):
	def __init__(self, name, expression, arg_name = None, annotations = None):
		super().__init__()
		if annotations is None:
			annotations = []
		self.annotations = annotations
		self.name = name
		if arg_name:
			expression.slot_list.append(ArgumentSlotNode(arg_name))
		self.expression = expression
		
	def __str__(self):
		return f"BinarySlot: (name='{self.name}' expression='{self.expression}' annotation='{'-'.join(self.annotations)}')"

	def interpret(self, context):
		return SelfSlot(self.name, self.expression.interpret(context), True, annotations=self.annotations)
	
	def verify_syntax(self):
		self.expression.set_allowable_argument_slot_count(1)
		self.expression.verify_syntax()