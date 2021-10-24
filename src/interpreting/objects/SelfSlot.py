from typing import OrderedDict
from interpreting.objects.SelfException import SelfException
import copy
from interpreting.objects.SelfObject import SelfObject
from Messages import *

class SelfSlot:
	def __init__(self, name, value=None, is_immutable=False, keyword_list=None):
		self.name = name
		self.value:SelfObject = value
		self.is_immutable = is_immutable
		self.keyword_list = keyword_list

	def __str__(self):
		return "SelfSlot:{{name='{}', value={{{}}}, is_immutable='{}', keyword_list='{}'}}".format(
			self.name, self.value, self.is_immutable, self.keyword_list
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

	def call_keyword_method(self, receiver, arg_list):
		if not self.keyword_list:
			raise SelfException(Messages.NOT_A_KEYWORD_SLOT.value)

		clone = copy.deepcopy(self.value)
		clone.parent_slots["self"] = SelfSlot("self", receiver, True)
		for i in range(len(self.keyword_list)):
			slot_name = list(self.value.arg_slots.keys())[i]
			clone.slots[slot_name] = SelfSlot(slot_name, arg_list[i])

		return self.value.code.interpret(clone)