from interpreting.objects.SelfObject import *
from interpreting.objects.SelfSlot import *

class RegularObjectNode:
	def __init__(self, slot_list=[]):
		self.slot_list = slot_list

	def __str__(self):
		return "RegularObject: (slot-list={})".format(list(map(str, self.slot_list)))

	def interpret(self, environment):
		interpreted_slot_list = {}
		for s in self.slot_list:
			interpreted_slot_list[s.name] = s.interpret(environment)
		return SelfObject(interpreted_slot_list)