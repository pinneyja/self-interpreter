from .Node import Node
from .DataSlotNode import DataSlotNode

class KeywordMessageNode(Node):
	def __init__(self, expression, keyword_list, value_list):
		super().__init__()
		self.message = ''.join(keyword_list)
		self.expression = expression
		self.keyword_list = keyword_list
		self.value_list = value_list

	def __str__(self):
		return f"KeywordMessage: (expression={self.expression} keyword_list={self.keyword_list} value_list={self.value_list})"

	def interpret(self, context):
		arg_list = [DataSlotNode(self.keyword_list[i], expression=self.value_list[i]).interpret(context) for i in range(len(self.keyword_list))]
		if self.expression:
			return self.expression.interpret(context).pass_keyword_message(self.message, arg_list)
		else:
			return context.pass_keyword_message(self.message, arg_list)