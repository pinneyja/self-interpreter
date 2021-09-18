from interpreting.objects.SelfObject import *

class Environment(SelfObject):
	def __init__(self, slots = {}):
		super().__init__(slots)