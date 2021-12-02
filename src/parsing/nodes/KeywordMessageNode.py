from .Node import Node
from .DataSlotNode import DataSlotNode
from .ResendNode import ResendNode

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
		if self.expression and type(self.expression) is not ResendNode:
			interpreted = self.expression.interpret(context)
			if interpreted.nonlocal_return:
				return interpreted

		arg_list = []
		for i in range(len(self.keyword_list)):
			interpreted_arg_value = self.value_list[i].interpret(context)
			if interpreted_arg_value.nonlocal_return:
				return interpreted_arg_value
			arg_list.append(interpreted_arg_value)

		if self.expression:
			if type(self.expression) is ResendNode:
				if (self.expression.receiver == "resend"):
					return context.parent_slots["self"].call_method(None).undirected_resend(self.message, arg_list)
				else:
					return context.parent_slots["self"].call_method(None).directed_resend(self.expression.receiver, self.message, arg_list)
			return interpreted.pass_keyword_message(self.message, arg_list)
		else:
			return context.pass_keyword_message(self.message, arg_list)

	def verify_syntax(self):
		if self.expression:
			self.expression.verify_syntax()
		for value in self.value_list:
			value.verify_syntax()