from typing import OrderedDict
from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.SelfSlot import SelfSlot
from parsing.nodes.Node import Node
from parsing.nodes.slot_nodes.ArgumentSlotNode import ArgumentSlotNode
from parsing.nodes.slot_nodes.ParentSlotNode import ParentSlotNode

class BlockNode(Node):
	def __init__(self, slot_list=None, code=None, annotated_slot_lists=None):
		super().__init__()

		if slot_list is None:
			slot_list = []

		if annotated_slot_lists is None:
			annotated_slot_lists = []

		self.slot_list = slot_list
		self.annotated_slot_lists=annotated_slot_lists
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
			block_method = SelfObject(interpreted_slot_list, interpreted_arg_slot_list, interpreted_parent_slot_list, self.code)
			block_method.is_block_method = True
			slots["value"] = SelfSlot("value", block_method, True)
		else:
			method_name = "value:" + "With:"*(len(interpreted_arg_slot_list) - 1)
			block_method = SelfObject(interpreted_slot_list, interpreted_arg_slot_list, interpreted_parent_slot_list, self.code)
			block_method.is_block_method = True
			slots[method_name] = SelfSlot(
				method_name, 
				block_method,
				True, 
				["value:"] + ["With:"]*(len(interpreted_arg_slot_list) - 1))

		return SelfObject(slots)
	
	def verify_syntax(self):
		for s in self.slot_list:
			s.verify_syntax()
		if self.code:
			self.code.verify_syntax()