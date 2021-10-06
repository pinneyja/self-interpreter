from typing import OrderedDict
from .SelfException import *

class SelfObject:
	def __init__(self, slots = None, arg_slots = None, code = None):
		if slots is None:
			slots = OrderedDict()
		
		if arg_slots is None:
			arg_slots = OrderedDict()
			 
		self.slots = slots
		self.arg_slots = arg_slots
		self.code = code

	def __str__(self):
		output  = "SelfObject:{Slots = ["
		for key in self.slots:
			output += "{},".format(self.slots[key])
		output += "], Argument Slots = ["
		for key in self.arg_slots:
			output += "{},".format(self.arg_slots[key])
		output += "], code={{{}}}".format(self.code)
		return output + "}"

	def pass_unary_message(self, message):
		if (not message in self.slots):
			return SelfException("Lookup error")
		return self.slots[message].get_value()

	def pass_binary_message(self, message, arg):
		if (not message in self.slots):
			return SelfException("Lookup error")
		return self.slots[message].get_value(arg)

	def pass_keyword_message(self, message, arg_dict):
		if (not message in self.slots):
			return SelfException("Lookup error")
		return self.slots[message].call_keyword_method(arg_dict)
