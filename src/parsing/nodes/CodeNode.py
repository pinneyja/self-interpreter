from .Node import Node

class CodeNode(Node):
	def __init__(self, expressions):
		super().__init__()
		self.expressions = expressions
		self.nonlocal_return = False
		self.contained_in_block = False

	def __str__(self):
		return f"Code: (expression_list={self.expressions}, nonlocal_return={self.nonlocal_return})"

	def interpret(self, context):
		for expression in self.expressions:
			result = expression.interpret(context)

			if result.nonlocal_return:
				if not self.contained_in_block:
					result.set_nonlocal_return(False)

				return result

		if self.nonlocal_return:
			result.set_nonlocal_return(True)

		return result

	def verify_syntax(self):
		for expression in self.expressions:
			expression.verify_syntax()

	def set_nonlocal_return(self, nonlocal_return):
		self.nonlocal_return = nonlocal_return

	def set_contained_in_block(self, contained_in_block):
		self.contained_in_block = contained_in_block