from typing import OrderedDict
from Messages import Messages
from interpreting.primitive_methods.PrimitiveDictionary import primitive_dict
from interpreting.objects.SelfException import SelfException
import copy

class SelfObject:
	def __init__(self, slots = None, arg_slots = None, parent_slots = None, code = None, annotation = None):
		if slots is None:
			slots = OrderedDict()
		
		if arg_slots is None:
			arg_slots = OrderedDict()
			 
		if parent_slots is None:
			parent_slots = OrderedDict()

		self.slots = slots
		self.arg_slots = arg_slots
		self.parent_slots = parent_slots
		self.annotation = annotation
		self.code = code
		self.nonlocal_return = False
		self.nonlocal_return_context = None
		self.is_block_method = False
		self.has_returned = False

	def __str__(self):
		output  = f"SelfObject:{{ '{self.annotation}' Slots = ["
		for key in self.slots:
			output += "{},".format(self.slots[key])
		output += "], Argument Slots = ["
		for key in self.arg_slots:
			output += "{},".format(self.arg_slots[key])
		output += "], Parent Slots = ["
		for key in self.parent_slots:
			output += "{},".format(self.parent_slots[key])
		output += "], code={{{}}}".format(self.code)
		output += f", nonlocal_return={self.nonlocal_return}" 
		return output + "}"

	def pass_unary_message(self, message):
		if message[0] == '_':
			return self.handle_primitive_method(message)
		matching_slot = self.lookup(message, set())
		
		return matching_slot.call_method(self)

	def pass_binary_message(self, message, arg):
		matching_slot = self.lookup(message, set())

		return matching_slot.call_method(self, [arg])

	def pass_keyword_message(self, message, arg_list):
		if message[0] == '_':
			return self.handle_primitive_method(message, arg_list)

		matching_slot = self.lookup(message, set())

		return matching_slot.call_method(self, arg_list)

	def handle_primitive_method(self, message, arg_list=None):
		if message not in primitive_dict:
			raise SelfException(Messages.PRIMITIVE_NOT_DEFINED.value.format(message))

		return primitive_dict[message](self, arg_list)

	def lookup(self, sel, V):
		M = self.lookup_helper(sel, V)
		if len(M) == 1:
			return M.pop()
		elif len(M) == 0:
			raise SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value.format(sel))
		else:
			raise SelfException(Messages.LOOKUP_ERROR_MULTIPLE_SLOTS.value.format(sel))

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

	def set_slot(self, slot_name, value):
		matching_slot = self.lookup(slot_name, set())
		if matching_slot.is_immutable:
			raise SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value.format(slot_name + ":"))
		else:
			matching_slot.value = value

	def set_nonlocal_return(self, nonlocal_return):
		self.nonlocal_return = nonlocal_return

	def undirected_resend(self, sel, arg_list=None):
		M = self.parent_lookup(sel, set())
		if len(M) == 0:
			raise SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value.format(sel))
		elif len(M) == 1:
			matching_slot = M.pop()
			return matching_slot.call_method(self, arg_list)
		else:
			raise SelfException(Messages.LOOKUP_ERROR_MULTIPLE_SLOTS.value.format(sel))

	def directed_resend(self, del_name, sel, arg_list=None):
		if del_name not in self.slots and del_name not in self.parent_slots:
			raise SelfException(Messages.NO_DELEGATEE_SLOT.value.format(del_name))
		
		if del_name in self.slots:
			matching_slot = self.slots[del_name].call_method(None).lookup(sel, set())
		else:
			matching_slot = self.parent_slots[del_name].call_method(None).lookup(sel, set())
		return matching_slot.call_method(self, arg_list)

	def clone(self):
		clone = copy.copy(self)
		clone.slots = {key : self.slots[key].clone() for key in self.slots}
		clone.arg_slots = {key : self.arg_slots[key].clone() for key in self.arg_slots}
		clone.parent_slots = {key : self.parent_slots[key].clone() for key in self.parent_slots}
		return clone