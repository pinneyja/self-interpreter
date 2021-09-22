from typing import OrderedDict
from .SelfException import *

class SelfObject:
	def __init__(self, slots = OrderedDict()):
		self.slots = slots

	def __str__(self):
		output  = "SelfObject:{"
		for key in self.slots:
			output += "{},".format(self.slots[key])
		return output + "}"

	def pass_unary_message(self, message):
		if (not message in self.slots):
			return SelfException("Lookup error")
		return self.slots[message].get_value()