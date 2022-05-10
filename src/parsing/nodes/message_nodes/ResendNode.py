from Messages import Messages
from interpreting.objects.SelfException import SelfException
from parsing.nodes.Node import Node

class ResendNode(Node):
	def __init__(self, receiver):
		super().__init__()
		self.receiver = receiver

	def __str__(self):
		return f"ResendNode: '{self.receiver}'"

	def interpret(self, context):
		pass

	def get_parent(self, context):
		if "self" in context.parent_slots:
			return context.parent_slots["self"]
		elif "" in context.parent_slots:
			return self.get_parent(context.parent_slots[""].value)
		else:
			raise SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value().format("self"))