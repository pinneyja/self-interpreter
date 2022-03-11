from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.SelfSlot import SelfSlot

class SelfObjectVector(SelfObject):
	def __init__(self, slots = None, arg_slots = None, parent_slots = None, code = None, annotation = None, code_string = None, alt_string = None, indexable = None):
		super().__init__(slots, arg_slots, parent_slots, code, annotation, code_string, alt_string)
		if indexable:
			self.indexable = indexable
		else:
			self.indexable = []

	def as_dict(self, visited):
		is_unvisited = self not in visited
		d = super().as_dict(visited)
		d["slots"] = {}
		for i in range(len(self.indexable)):
			new_visited = visited.copy()
			name = "<" + str(i) + ">"
			slot = SelfSlot(name, self.indexable[i])
			d["slots"][name] = slot.as_dict(new_visited, is_unvisited)
		return d