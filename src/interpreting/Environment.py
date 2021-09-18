from interpreting.objects.Object import *

class Environment(Object):
	def __init__(self, slots = {}):
		super().__init__(slots)