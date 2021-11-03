from interpreting.objects.SelfSlot import *
from parsing.nodes.ArgumentSlotNode import ArgumentSlotNode
from parsing.nodes.RegularObjectNode import RegularObjectNode
from .Node import Node
from parsing.SelfParsingError import *
from Messages import *

class KeywordSlotNode(Node):
	def __init__(self, keyword_list, object, arg_list=None):
		super().__init__()
				
		if arg_list is None:
			arg_list = []

		self.arg_list = arg_list

		self.name = ''.join(keyword_list)
		object.slot_list += [ArgumentSlotNode(arg) for arg in arg_list]
		self.object = object
		self.keyword_list = keyword_list

	def __str__(self):
		return f"KeywordSlot: (keyword_list={self.keyword_list} object={self.object})"

	def interpret(self, context):
		return SelfSlot(self.name, self.object.interpret(context), True, self.keyword_list)

	def verify_syntax(self):
		arg_list_as_set = set(self.arg_list)
		if self.arg_list and len(arg_list_as_set) != len(self.arg_list):
			for arg in self.arg_list:
				if arg in arg_list_as_set:
					arg_list_as_set.remove(arg)
				else:
					raise SelfParsingError(Messages.SLOT_ALREADY_DEFINED.value.format(arg))

		self.object.set_allowable_argument_slot_count(len(self.keyword_list))
		self.object.verify_syntax()