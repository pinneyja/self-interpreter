from Messages import Messages
from interpreting.objects.SelfException import SelfException
from parsing.nodes.Node import Node

class CodeNode(Node):
	def __init__(self, expressions):
		super().__init__()
		self.expressions = expressions
		self.has_caret = False
		self.contained_in_block = False

	def __str__(self):
		return f"Code: (expression_list={self.expressions}, has_caret={self.has_caret})"

	def interpret(self, context):
		return_context = None
		if self.contained_in_block:
			return_context = context.parent_slots[""].value
			while return_context.is_block_method:
				return_context = return_context.parent_slots[""].value
			if return_context.has_returned:
				raise SelfException(Messages.ENCLOSING_METHOD_HAS_RETURNED.value)

		for expression in self.expressions:
			result = expression.interpret(context)
			if result.nonlocal_return:
				if result.nonlocal_return_context is context:
					result.set_nonlocal_return(False)

				return result

		result.nonlocal_return_context = return_context

		if self.has_caret and self.contained_in_block:
			result.set_nonlocal_return(True)

		return result

	def verify_syntax(self):
		for expression in self.expressions:
			expression.verify_syntax()

	def set_has_caret(self, has_caret):
		self.has_caret = has_caret

	def set_contained_in_block(self, contained_in_block):
		self.contained_in_block = contained_in_block