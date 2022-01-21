from interpreting.objects.SelfException import SelfException
from interpreting.objects.SelfSlot import SelfSlot
from parsing.nodes.Node import Node
from interpreting.objects.primitive_objects.SelfLobby import SelfLobby

class DataSlotNode(Node):
	def __init__(self, name, operator = None, expression = None, annotations = None):
		super().__init__()
		if annotations is None:
			annotations = []
		self.annotations = annotations
		self.name = name
		self.operator = operator
		self.expression = expression

	def __str__(self):
		return f"DataSlot: (name='{self.name}' operator='{self.operator}' expression='{self.expression}' annotation='{'-'.join(self.annotations)}')"

	def interpret(self, context):
		if (not self.expression):
			try:
				lobby = SelfLobby.get_lobby()
				globals = lobby.parent_slots["globals"].value
				nil = globals.pass_unary_message("nil")
				self.expression = nil
			except:
				pass
			return SelfSlot(self.name, self.expression, annotations=self.annotations)
		else:
			return SelfSlot(self.name, self.expression.interpret(context), self.operator == "=", annotations=self.annotations)

	def verify_syntax(self):
		if self.expression:
			self.expression.verify_syntax()