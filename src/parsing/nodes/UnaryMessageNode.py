from .Node import Node

class UnaryMessageNode(Node):
	def __init__(self, expression, message):
		super().__init__()
		self.expression = expression
		self.message = message

	def __str__(self):
		return "UnaryMessage: (expression={} message='{}')".format(self.expression, self.message)

	def interpret(self, context):
		if self.expression:
			return self.expression.interpret(context).pass_unary_message(self.message)
		else:
			return context.pass_unary_message(self.message)

	def verify_syntax(self):
		if self.expression:
			self.expression.verify_syntax()