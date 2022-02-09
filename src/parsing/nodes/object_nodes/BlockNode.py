from typing import OrderedDict
from parsing.nodes.Node import Node
from parsing.nodes.object_nodes.RegularObjectNode import RegularObjectNode
from parsing.nodes.CodeNode import CodeNode

class BlockNode(Node):
	def __init__(self, slot_list=None, code=None, code_string=None):
		super().__init__()

		if slot_list is None:
			slot_list = []

		self.slot_list = slot_list
		self.code = code
		self.code_string = f"[{code_string}]"

		if self.code:
			self.code.set_contained_in_block(True)
		else:
			self.code = CodeNode([RegularObjectNode()])

	def __str__(self):
		return f"BlockObject: (slot-list={self.slot_list} code={{{self.code}}})"

	def interpret(self, context):
		return RegularObjectNode(self.slot_list, self.code, code_string=self.code_string, block_node=True).interpret(context)
	
	def verify_syntax(self):
		for s in self.slot_list:
			s.verify_syntax()
		if self.code:
			self.code.verify_syntax()