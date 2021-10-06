from .Node import Node

class BinaryMessageNode(Node):
	def __init__(self, expression, message, arg_expression):
		super().__init__()
		self.expression = expression
		self.message = message
		self.arg_expression = arg_expression

	def __str__(self):
		return "BinaryMessage: (expression={} message='{}' arg_expression='{}')".format(self.expression, self.message, self.arg_expression)

	def interpret(self, context):
		if self.expression:
			return self.expression.interpret(context).pass_binary_message(self.message, self.arg_expression.interpret(context))
		else:
			return context.pass_binary_message(self.message, self.arg_expression)