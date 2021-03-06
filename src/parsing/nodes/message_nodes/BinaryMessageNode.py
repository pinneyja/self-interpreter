from parsing.nodes.Node import Node
from parsing.nodes.message_nodes.ResendNode import ResendNode

class BinaryMessageNode(Node):
	def __init__(self, expression, message, arg_expression):
		super().__init__()
		self.expression = expression
		self.message = message
		self.arg_expression = arg_expression

	def __str__(self):
		return "BinaryMessage: (expression={} message='{}' arg_expression='{}')".format(self.expression, self.message, self.arg_expression)

	def interpret(self, context):
		interpreted_arg = self.arg_expression.interpret(context)
		if self.expression:
			if type(self.expression) is ResendNode:
				if self.expression.receiver == "resend":
					return context.undirected_resend(self.message, [interpreted_arg])
				else:
					return context.directed_resend(self.expression.receiver, self.message, [interpreted_arg])

			interpreted = self.expression.interpret(context)
			if interpreted.nonlocal_return:
				return interpreted
			if interpreted_arg.nonlocal_return:
				return interpreted_arg
			return interpreted.pass_binary_message(self.message, interpreted_arg)
		else:
			if interpreted_arg.nonlocal_return:
				return interpreted_arg
			if self.message in context.slots or self.message in context.parent_slots or self.message in context.arg_slots:
				return context.pass_binary_message(self.message, interpreted_arg)
			elif "self" in context.parent_slots and not context.is_block_method:
				return context.parent_slots["self"].value.pass_binary_message(self.message, interpreted_arg)
			else:
				if "" in context.parent_slots and (self.message in context.parent_slots[""].value.slots or self.message in context.parent_slots[""].value.parent_slots or self.message in context.parent_slots[""].value.arg_slots):
					return context.parent_slots[""].value.pass_binary_message(self.message, interpreted_arg)
				while not "self" in context.parent_slots[""].value.parent_slots:
					context = context.parent_slots[""].value
					if "" in context.parent_slots and (self.message in context.parent_slots[""].value.slots or self.message in context.parent_slots[""].value.parent_slots or self.message in context.parent_slots[""].value.arg_slots):
						return context.parent_slots[""].value.pass_binary_message(self.message, interpreted_arg)
				return context.parent_slots[""].value.parent_slots["self"].value.pass_binary_message(self.message, interpreted_arg)

	def verify_syntax(self):
		if self.expression:
			self.expression.verify_syntax()

		self.arg_expression.verify_syntax()