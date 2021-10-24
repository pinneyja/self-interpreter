from parsing.Parser import *
from interpreting.objects.SelfException import *
from parsing.SelfParsingError import *
from Messages import *
from interpreting.objects.SelfLobby import *

class Interpreter:
	def __init__(self):
		self.lobby = SelfLobby()

	def interpret(self, syntaxTree):
		try:
			result = syntaxTree.interpret(self.lobby)
		except (SelfException, SelfParsingError) as e:
			raise e
		except Exception as e:
			raise SelfException(Messages.GENERIC_ERROR.value.format(str(e)))
		return result