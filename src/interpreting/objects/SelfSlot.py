import copy
from interpreting.objects.SelfObject import SelfObject

class SelfSlot:
	def __init__(self, name, value=None, is_immutable=False, keyword_list=None, annotations=None):
		if annotations is None:
			annotations = []
		self.name = name
		self.value:SelfObject = value
		self.is_immutable = is_immutable
		self.keyword_list = keyword_list
		self.annotations = [] + annotations

	def __str__(self):
		return f"SelfSlot:{{name='{self.name}', value={{{self.value}}}, is_immutable='{self.is_immutable}', keyword_list='{self.keyword_list}', annotations='{'-'.join(self.annotations)}'}}"
	
	def __repr__(self):
		return self.__str__()

	def call_method(self, receiver, args=None):
		if self.value.code:
			clone = copy.copy(self.value)
			clone.parent_slots["self"] = SelfSlot("self", receiver, True)
			for i, key in enumerate(clone.arg_slots):
				clone.slots[key] = SelfSlot(key, args[i])
			result = self.value.code.interpret(clone)
			clone.has_returned = True
			return result
		else:
			return self.value

	def clone(self):
		return copy.copy(self)