from interpreting.objects.SelfObject import SelfObject

def SelfBoolean(bool):
	if bool:
		return SelfTrue.instance()
	else:
		return SelfFalse.instance()

class SelfTrue(SelfObject):
	_instance = None

	def __init__(self):
		if SelfTrue._instance:
			raise Exception("This class is a singleton!")
		else:
			super().__init__()
			SelfTrue._instance = self

	def __str__(self):
		return "true"

	def get_value(self):
		return True

	@staticmethod
	def instance():
		if  SelfTrue._instance:
			return SelfTrue._instance
		else:
			return SelfTrue()

class SelfFalse(SelfObject):
	_instance = None

	def __init__(self):
		if SelfFalse._instance:
			raise Exception("This class is a singleton!")
		else:
			super().__init__()
			SelfFalse._instance = self

	def __str__(self):
		return "false"

	def get_value(self):
		return False

	@staticmethod
	def instance():
		if  SelfFalse._instance:
			return SelfFalse._instance
		else:
			return SelfFalse()