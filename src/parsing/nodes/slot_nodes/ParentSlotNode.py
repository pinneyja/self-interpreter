from interpreting.objects.SelfSlot import SelfSlot
from parsing.nodes.Node import Node

class ParentSlotNode(Node):
	def __init__(self, name, operator = None, expression = None, annotations = None):
		super().__init__()
		if annotations is None:
			annotations = []
		self.annotations = annotations
		self.name = name
		self.operator = operator
		self.expression = expression

	def __str__(self):
		return f"ParentSlot: (name='{self.name}' operator='{self.operator}' expression='{self.expression}' annotation='{'-'.join(self.annotations)}')"

	def interpret(self, context):
		if (not self.expression):
			return SelfSlot(self.name)
		else:
			return SelfSlot(self.name, self.expression.interpret(context), self.operator == "=", annotations=self.annotations)

	def verify_syntax(self):
		if self.expression:
			self.expression.verify_syntax()