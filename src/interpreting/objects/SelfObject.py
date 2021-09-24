from typing import OrderedDict
from .SelfException import *

class SelfObject:
	def __init__(self, slots = OrderedDict(), code = None):
		self.slots = slots
		self.code = code

	def __str__(self):
		output  = "SelfObject:{["
		for key in self.slots:
			output += "{},".format(self.slots[key])
		output += "], code={{{}}}".format(self.code)
		return output + "}"

	def pass_unary_message(self, message):
		if (not message in self.slots):
			return SelfException("Lookup error")
		return self.slots[message].get_value()