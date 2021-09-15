class RegularObjectNode:
	def __init__(self, slot_list = []):
		self.slot_list = slot_list

	def __str__(self):
		return "RegularObject: slot-list='{}'".format(list(map(str, self.slot_list)))