from interpreting.objects.SelfObject import *
from parsing.nodes.ArgumentSlotNode import *

class RegularObjectNode:
	def __init__(self, slot_list=[], code=None):
		self.slot_list = slot_list
		self.code = code

	def __str__(self):
		return "RegularObject: (slot-list={} code={{{}}})".format(list(map(str, self.slot_list)), self.code)

	def interpret(self, context):
		interpreted_slot_list = OrderedDict()
		interpreted_arg_slot_list = OrderedDict()
		for s in self.slot_list:
			if type(s) is ArgumentSlotNode:
				interpreted_arg_slot_list[s.name] = s.interpret(context)
			else:
				interpreted_slot_list[s.name] = s.interpret(context)
		return SelfObject(interpreted_slot_list, interpreted_arg_slot_list, self.code)