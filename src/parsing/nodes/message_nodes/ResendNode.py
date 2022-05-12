from parsing.nodes.Node import Node

class ResendNode(Node):
	def __init__(self, receiver):
		super().__init__()
		self.receiver = receiver

	def __str__(self):
		return f"ResendNode: '{self.receiver}'"

	def interpret(self, context):
		pass