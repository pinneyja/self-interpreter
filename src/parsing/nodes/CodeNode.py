from .Node import Node

class CodeNode(Node):
	def __init__(self, expressions):
		super().__init__()
		self.expressions = expressions

	def __str__(self):
		return f"Code: (expression_list={self.expressions})"

	def interpret(self, context):
		return [expression.interpret(context) for expression in self.expressions][-1]

	def verify_syntax(self):
		for expression in self.expressions:
			expression.verify_syntax()