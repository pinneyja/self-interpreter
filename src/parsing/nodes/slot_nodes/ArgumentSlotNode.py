from interpreting.objects.SelfSlot import SelfSlot
from parsing.nodes.Node import Node

class ArgumentSlotNode(Node):
	def __init__(self, name, annotations = None):
		if annotations is None:
			annotations = []
		self.annotations = annotations
		self.name = name

	def __str__(self):
		return f"ArgumentSlot: (name='{self.name}' annotation='{'-'.join(self.annotations)}')"

	def interpret(self, context):
		return SelfSlot(self.name, annotations=self.annotations)