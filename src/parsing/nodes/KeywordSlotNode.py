from interpreting.objects.SelfSlot import *
from parsing.nodes.ArgumentSlotNode import ArgumentSlotNode
from parsing.nodes.RegularObjectNode import RegularObjectNode
from .Node import Node

class KeywordSlotNode(Node):
	def __init__(self, keyword_list, object, arg_list=None):
		super().__init__()
				
		if arg_list is None:
			arg_list = []

		self.name = ''.join(keyword_list)
		object.slot_list += [ArgumentSlotNode(arg) for arg in arg_list]
		self.object = object
		self.keyword_list = keyword_list

	def __str__(self):
		return f"KeywordSlot: (keyword_list={self.keyword_list} object={self.object})"

	def interpret(self, context):
		return SelfSlot(self.name, self.object.interpret(context), True, self.keyword_list)