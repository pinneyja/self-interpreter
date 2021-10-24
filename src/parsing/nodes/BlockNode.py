from interpreting.objects.SelfObject import *
from parsing.nodes.RegularObjectNode import *
from .Node import Node
from parsing.nodes.ArgumentSlotNode import *
from parsing.nodes.ParentSlotNode import *

class BlockNode(Node):
	def __init__(self, slot_list=None, code=None):
		super().__init__()

		if slot_list is None:
			slot_list = []

		self.slot_list = slot_list
		self.code = code

		if self.code:
			self.code.set_contained_in_block(True)

	def __str__(self):
		return f"BlockObject: (slot-list={self.slot_list} code={{{self.code}}})"

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

		slots = OrderedDict()
		interpreted_parent_slot_list[""] = SelfSlot("", context, True)
		if len(interpreted_arg_slot_list) == 0:
			slots["value"] = SelfSlot("value", SelfObject(interpreted_slot_list, interpreted_arg_slot_list, interpreted_parent_slot_list, self.code), True)
		else:
			method_name = "value:" + "With:"*(len(interpreted_arg_slot_list) - 1)
			slots[method_name] = SelfSlot(
				method_name, 
				SelfObject(interpreted_slot_list, interpreted_arg_slot_list, interpreted_parent_slot_list, self.code), 
				True, 
				["value:"] + ["With:"]*(len(interpreted_arg_slot_list) - 1))

		return SelfObject(slots)