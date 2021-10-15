from typing import OrderedDict
from interpreting.objects.SelfException import SelfException
import copy
from interpreting.objects.SelfObject import SelfObject

class SelfSlot:
	def __init__(self, name, value=None, isImmutable=False, keyword_list=None):
		self.name = name
		self.value:SelfObject = value
		self.isImmutable = isImmutable
		self.keyword_list = keyword_list

	def __str__(self):
		return "SelfSlot:{{name='{}', value={{{}}}, isImmutable='{}', keyword_list='{}'}}".format(
			self.name, self.value, self.isImmutable, self.keyword_list
		)

	def get_value(self, receiver, arg=None):
		if self.value.code:
			clone = copy.deepcopy(self.value)
			clone.parent_slots["self"] = SelfSlot("self", receiver, True)
			for key in clone.arg_slots:
				clone.slots[key] = SelfSlot(key, arg)
			return self.value.code.interpret(clone)
		else:
			return self.value

	def call_keyword_method(self, receiver, arg_dict):
		if not self.keyword_list:
			return SelfException("Not a keyword slot")

		if len(self.keyword_list) != len(self.value.arg_slots):
			return SelfException("Invalid number of argument slots")
			
		clone = copy.deepcopy(self.value)
		clone.parent_slots["self"] = SelfSlot("self", receiver, True)
		for i in range(len(self.keyword_list)):
			clone.slots[list(self.value.arg_slots.keys())[i]] = arg_dict[self.keyword_list[i]] 

		return self.value.code.interpret(clone)