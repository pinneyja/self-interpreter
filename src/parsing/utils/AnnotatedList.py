class AnnotatedList():
	def __init__(self, annotation, slot_list):
		self.annotation = annotation.value
		self.slot_list = slot_list

	def get_slots(self, annotations):
		annotations.append(self.annotation)
		slot_list = []
		for s in self.slot_list:
			if type(s) is AnnotatedList:
				slot_list += s.get_slots([] + annotations)
			else:
				s.annotations = [] + annotations
				slot_list.append(s)
		return slot_list
