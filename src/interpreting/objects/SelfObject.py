from typing import OrderedDict
from Messages import Messages
from interpreting.primitive_methods.PrimitiveDictionary import primitive_dict
from interpreting.objects.SelfException import SelfException
import copy

class SelfObject:
	def __init__(self, slots = None, arg_slots = None, parent_slots = None, code = None, annotation = None, code_string = None, alt_string = None, declared_ctx = None):
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
		self.code_string = code_string
		self.alt_string = alt_string
		self.gui_representation = None
		self.name = None
		self.declared_ctx:SelfObject = declared_ctx

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
			declared_ctx = self
			if "l " in declared_ctx.slots:
				declared_ctx = declared_ctx.slots["l "].value

			if (sel in self.slots):
				self.slots[sel].declared_ctx = declared_ctx
				return {self.slots[sel]}
			elif (sel in self.parent_slots):
				
				self.parent_slots[sel].declared_ctx = declared_ctx
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
		run_ctx = self.get_non_block_parent()
		M = self.declared_ctx.parent_lookup(sel, set())
		if len(M) == 0:
			raise SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value.format(sel))
		elif len(M) == 1:
			matching_slot = M.pop()
			return matching_slot.call_method(run_ctx, arg_list)
		else:
			raise SelfException(Messages.LOOKUP_ERROR_MULTIPLE_SLOTS.value.format(sel))

	def directed_resend(self, del_name, sel, arg_list=None):
		run_ctx = self.get_non_block_parent()
		if del_name not in self.declared_ctx.slots and del_name not in self.declared_ctx.parent_slots:
			raise SelfException(Messages.NO_DELEGATEE_SLOT.value.format(del_name))
		
		if del_name in self.declared_ctx.slots:
			matching_slot = self.declared_ctx.slots[del_name].value.lookup(sel, set())
		else:
			matching_slot = self.declared_ctx.parent_slots[del_name].value.lookup(sel, set())
		return matching_slot.call_method(run_ctx, arg_list)
	
	def copy_slots_of(self, self_obj):
		self.slots = self_obj.slots
		self.arg_slots = self_obj.arg_slots
		self.parent_slots = self_obj.parent_slots

	def clone(self):
		clone = copy.copy(self)
		clone.slots = {key : self.slots[key].clone() for key in self.slots}
		clone.arg_slots = {key : self.arg_slots[key].clone() for key in self.arg_slots}
		clone.parent_slots = {key : self.parent_slots[key].clone() for key in self.parent_slots}
		clone.gui_representation = None
		return clone

	def as_dict(self, visited):
		from interpreting.printingutils.PrinterConfig import CONFIG
		is_unvisited = self not in visited
		visited.append(self)

		i = [0]
		def length_check(i):
			i[0] += 1
			return i[0] - 1 < CONFIG['MAX_LIST_LENGTH'] + 2

		parent_slots = {key + '*' : self.parent_slots[key].as_dict(visited, is_unvisited) for key in self.parent_slots if length_check(i)}
		arg_slots = {':' + key : self.arg_slots[key].as_dict(visited, is_unvisited) for key in self.arg_slots if length_check(i)}
		slots = {key : self.slots[key].as_dict(visited, is_unvisited) for key in self.slots if key not in self.arg_slots if length_check(i)}
		all_slots = parent_slots
		all_slots.update(arg_slots)
		all_slots.update(slots)
		
		if "*" in all_slots:
			all_slots["(parent)*"] = all_slots["*"]
			all_slots.pop("*")

		if "l " in all_slots:
			all_slots["(lexicalParent)"] = all_slots["l "]
			all_slots.pop("l ")

		dict = {
			'type' : self.__class__.__name__,
			'annotation' : self.annotation,
			'slots' : all_slots,
			'code_string' : self.code_string,
			'code' : self.code,
			'alt_string' : False 
		}

		if self.alt_string:
			dict['alt_string'] = True
		return dict

	def get_name(self):
		if self.name:
			return self.name
		else:
			return "a slots object"

	def get_non_block_parent(self):
		if "self" in self.parent_slots:
			return self.parent_slots['self'].value
		elif "" in self.parent_slots:
			return self.parent_slots[""].value.get_non_block_parent()
		else:
			raise SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value().format("self"))