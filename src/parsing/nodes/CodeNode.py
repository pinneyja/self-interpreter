from .Node import Node

class CodeNode(Node):
	def __init__(self, expressions):
		super().__init__()
		self.expressions = expressions

	def __str__(self):
		return f"Code: (expression_list={self.expressions})"

	def interpret(self, context):
		return [x.interpret(context) for x in self.expressions][-1]