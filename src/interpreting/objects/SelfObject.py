from typing import OrderedDict
from interpreting.PrimitiveDictionary import primitive_dict
from .SelfException import *
from Messages import *

class SelfObject:
	def __init__(self, slots = None, arg_slots = None, parent_slots = None, code = None):
		if slots is None:
			slots = OrderedDict()
		
		if arg_slots is None:
			arg_slots = OrderedDict()
			 
		if parent_slots is None:
			parent_slots = OrderedDict()

		self.slots = slots
		self.arg_slots = arg_slots
		self.parent_slots = parent_slots
		self.code = code

	def __str__(self):
		output  = "SelfObject:{Slots = ["
		for key in self.slots:
			output += "{},".format(self.slots[key])
		output += "], Argument Slots = ["
		for key in self.arg_slots:
			output += "{},".format(self.arg_slots[key])
		output += "], Parent Slots = ["
		for key in self.parent_slots:
			output += "{},".format(self.parent_slots[key])
		output += "], code={{{}}}".format(self.code)
		return output + "}"

	def pass_unary_message(self, message):
		matching_slot = self.lookup(message, set())
		if type(matching_slot) is SelfException:
			return matching_slot

		return matching_slot.get_value(self)

	def pass_binary_message(self, message, arg):
		matching_slot = self.lookup(message, set())
		if type(matching_slot) is SelfException:
			return matching_slot

		return matching_slot.get_value(self, arg)

	def pass_keyword_message(self, message, arg_list):
		if message[0] == '_':
			return self.handle_primitive_method(message, arg_list)

		matching_slot = self.lookup(message, set())
		if type(matching_slot) is SelfException:
			return matching_slot

		return matching_slot.call_keyword_method(self, arg_list)

	def handle_primitive_method(self, message, arg_list):
		if message not in primitive_dict:
			raise SelfException(Messages.PRIMITIVE_NOT_DEFINED.value.format(message))

		return primitive_dict[message](self, arg_list)

	def lookup(self, sel, V):
		M = self.lookup_helper(sel, V)
		if len(M) == 1:
			return M.pop()
		elif len(M) == 0:
			raise SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value)
		else:
			raise SelfException(Messages.LOOKUP_ERROR_MULTIPLE_SLOTS.value)

	def lookup_helper(self, sel, V):
		if self in V:
			return set()
		else:
			if (sel in self.slots):
				return {self.slots[sel]}
			elif (sel in self.parent_slots):
				return {self.parent_slots[sel]}
			else:
				return self.parent_lookup(sel, V)

	def parent_lookup(self, sel, V):
		M = set()
		for parent_slot_name in self.parent_slots:
			M = M.union(self.parent_slots[parent_slot_name].value.lookup_helper(sel, V.union({self})))
		return M