from interpreting.objects.SelfObject import *
from .Node import Node
from parsing.nodes.ArgumentSlotNode import *
from parsing.nodes.ParentSlotNode import *

class RegularObjectNode(Node):
	def __init__(self, slot_list=None, code=None):
		super().__init__()

		if slot_list is None:
			slot_list = []

		self.slot_list = slot_list
		self.code = code

	def __str__(self):
		return f"RegularObject: (slot-list={self.slot_list} code={{{self.code}}})"

	def interpret(self, context):
		interpreted_slot_list = OrderedDict()
		interpreted_arg_slot_list = OrderedDict()
		interpreted_parent_slot_list = OrderedDict()
		for s in self.slot_list:
			if type(s) is ArgumentSlotNode:
				interpreted_arg_slot_list[s.name] = s.interpret(context)
			elif type(s) is ParentSlotNode:
				interpreted_parent_slot_list[s.name] = s.interpret(context)
			else:
				interpreted_slot_list[s.name] = s.interpret(context)
		return SelfObject(interpreted_slot_list, interpreted_arg_slot_list, interpreted_parent_slot_list, self.code)