class UnaryMessageNode:
	
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message

	def __str__(self):
		return "UnaryMessage: (expression={} message='{}')".format(self.expression, self.message)

	def interpret(self, environment):
		return self.expression.interpret(environment).pass_unary_message(self.message)

