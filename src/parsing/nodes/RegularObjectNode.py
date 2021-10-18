from interpreting.objects.SelfObject import *
from .Node import Node
from parsing.nodes.ArgumentSlotNode import *
from parsing.nodes.ParentSlotNode import *
from parsing.SelfParsingError import *
from Messages import *

class RegularObjectNode(Node):
	def __init__(self, slot_list=None, code=None):
		super().__init__()

		if slot_list is None:
			slot_list = []

		self.slot_list = slot_list
		self.code = code
		self.allowable_argument_slot_count = 0

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
	
	def set_allowable_argument_slot_count(self, allowable_argument_slot_count):
		self.allowable_argument_slot_count = allowable_argument_slot_count

	def verify_syntax(self):
		if self.code:
			self.code.verify_syntax()

		for slot in self.slot_list:
			slot.verify_syntax()

		argument_slot_count = 0
		for slot in self.slot_list:
			if type(slot) is ArgumentSlotNode:
				argument_slot_count += 1

		if argument_slot_count != self.allowable_argument_slot_count:
			raise SelfParsingError(Messages.INVALID_NUMBER_ARG_SLOTS.value)
		if argument_slot_count != 0 and self.code is None:
			raise SelfParsingError(Messages.EMPTY_OBJECT_WITH_ARG.value)