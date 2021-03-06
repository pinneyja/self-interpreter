from parsing.nodes.Node import Node
from parsing.nodes.message_nodes.ResendNode import ResendNode

class UnaryMessageNode(Node):
	def __init__(self, expression, message):
		super().__init__()
		self.expression = expression
		self.message = message

	def __str__(self):
		return "UnaryMessage: (expression={} message='{}')".format(self.expression, self.message)

	def interpret(self, context):
		if self.expression:
			if type(self.expression) is ResendNode:
				if self.expression.receiver == "resend":
					return context.undirected_resend(self.message)
				else:
					return context.directed_resend(self.expression.receiver, self.message)

			interpreted = self.expression.interpret(context)
			if interpreted.nonlocal_return:
				return interpreted
			return interpreted.pass_unary_message(self.message)
		else:
			if self.message in context.slots or self.message in context.parent_slots or self.message in context.arg_slots:
				return context.pass_unary_message(self.message)
			elif "self" in context.parent_slots and not context.is_block_method:
				return context.parent_slots["self"].value.pass_unary_message(self.message)
			else:
				if "" in context.parent_slots and (self.message in context.parent_slots[""].value.slots or self.message in context.parent_slots[""].value.parent_slots or self.message in context.parent_slots[""].value.arg_slots):
					return context.parent_slots[""].value.pass_unary_message(self.message)
				while not "self" in context.parent_slots[""].value.parent_slots:
					context = context.parent_slots[""].value
					if "" in context.parent_slots and (self.message in context.parent_slots[""].value.slots or self.message in context.parent_slots[""].value.parent_slots or self.message in context.parent_slots[""].value.arg_slots):
						return context.parent_slots[""].value.pass_unary_message(self.message)
				return context.parent_slots[""].value.parent_slots["self"].value.pass_unary_message(self.message)

	def verify_syntax(self):
		if self.expression:
			self.expression.verify_syntax()