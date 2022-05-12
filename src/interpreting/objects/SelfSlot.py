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
		self.declared_ctx:SelfObject = None

	def __str__(self):
		return f"SelfSlot:{{name='{self.name}', value={{{self.value}}}, is_immutable='{self.is_immutable}', keyword_list='{self.keyword_list}', annotations='{'-'.join(self.annotations)}'}}"
	
	def __repr__(self):
		return self.__str__()

	def call_method(self, receiver, args=None):
		if self.value.code:
			clone = self.value.clone()
			if not clone.is_block_method:
				clone.parent_slots["self"] = SelfSlot("self", receiver, True)
			for i, key in enumerate(clone.arg_slots):
				clone.slots[key] = SelfSlot(key, args[i])
			clone.declared_ctx = self.declared_ctx
			clone.code = None
			result = self.value.code.interpret(clone)
			clone.has_returned = True
			return result
		else:
			return self.value

	def clone(self):
		return copy.copy(self)

	def as_dict(self, visited, include_value):
		dict = {
			'type' : self.__class__.__name__,
			'name' : self.name,
			'annotations' : self.annotations,
			'value' : self.value.as_dict(visited) if self.value and include_value else None,
			'is_immutable' : self.is_immutable
		}
		return dict