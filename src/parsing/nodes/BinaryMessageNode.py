from .Node import *
from .RegularObjectNode import *

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
					return context.parent_slots["self"].call_method(None).undirected_resend(self.message, [interpreted_arg])
				else:
					return context.parent_slots["self"].call_method(None).directed_resend(self.expression.receiver, self.message, [interpreted_arg])

			interpreted = self.expression.interpret(context)
			if interpreted.nonlocal_return:
				return interpreted
			if interpreted_arg.nonlocal_return:
				return interpreted_arg
			return interpreted.pass_binary_message(self.message, interpreted_arg)
		else:
			if interpreted_arg.nonlocal_return:
				return interpreted_arg
			return context.pass_binary_message(self.message, interpreted_arg)

	def verify_syntax(self):
		if self.expression:
			self.expression.verify_syntax()

		self.arg_expression.verify_syntax()