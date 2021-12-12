from typing import OrderedDict
from Messages import Messages
from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.SelfSlot import SelfSlot
from parsing.SelfParsingError import SelfParsingError
from parsing.nodes.Node import Node
from parsing.nodes.message_nodes.KeywordMessageNode import KeywordMessageNode
from parsing.nodes.message_nodes.UnaryMessageNode import UnaryMessageNode
from parsing.nodes.object_nodes.StringNode import StringNode
from parsing.nodes.slot_nodes.ArgumentSlotNode import ArgumentSlotNode
from parsing.nodes.slot_nodes.DataSlotNode import DataSlotNode
from parsing.nodes.slot_nodes.ParentSlotNode import ParentSlotNode
from parsing.utils.AnnotatedList import AnnotatedList

class RegularObjectNode(Node):
	def __init__(self, slot_list_annotated=None, code=None, object_annotation=None):
		super().__init__()
		slot_list = []
		if slot_list_annotated is not None:
			for s in slot_list_annotated:
				if type(s) is AnnotatedList:
					slot_list += s.get_slots([])
				else:
					slot_list.append(s)

		self.object_annotation = None
		if object_annotation is not None:
			self.object_annotation = object_annotation.value

		self.slot_list = slot_list
		self.code = code
		self.allowable_argument_slot_count = 0

	def __str__(self):
		return f"RegularObject: (annotation='{self.object_annotation}' slot-list={self.slot_list} code={{{self.code}}})"

	def interpret(self, context):
		interpreted_slot_list = OrderedDict()
		interpreted_arg_slot_list = OrderedDict()
		interpreted_parent_slot_list = OrderedDict()

		for slot in self.slot_list:
			interpreted_slot = slot.interpret(context)
			if type(slot) is ArgumentSlotNode:
				interpreted_arg_slot_list[slot.name] = interpreted_slot
			elif type(slot) is ParentSlotNode:
				interpreted_parent_slot_list[slot.name] = interpreted_slot
			else:
				interpreted_slot_list[slot.name] = interpreted_slot

			if type(slot) is ParentSlotNode or type(slot) is DataSlotNode:
				if slot.operator == "<-" or slot.operator is None:
					slot_name = f"{slot.name}:"
					arg_slot_name = "arg"
					arg_slots = OrderedDict()
					arg_slots[arg_slot_name] = SelfSlot(arg_slot_name)
					code = KeywordMessageNode(None, ["_Assignment:", "Value:"], [StringNode(slot.name), UnaryMessageNode(None, arg_slot_name)])
					interpreted_slot_list[slot_name] = SelfSlot(slot_name, SelfObject(arg_slots=arg_slots, code=code), keyword_list=[slot_name])

		return SelfObject(interpreted_slot_list, interpreted_arg_slot_list, interpreted_parent_slot_list, self.code, self.object_annotation)
	
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