from parsing.Parser import *
from interpreting.objects.SelfException import *
from parsing.SelfParsingError import *
from Messages import *
from interpreting.objects.primitive_objects.SelfLobby import *

class Interpreter:
	def __init__(self, lobby=None):
		if not lobby:
			lobby = SelfLobby()
		self.lobby = lobby

	def interpret(self, syntaxTree):
		try:
			result = syntaxTree.interpret(self.lobby)
		except (SelfException, SelfParsingError) as e:
			raise e
		except Exception as e:
			raise SelfException(Messages.GENERIC_ERROR.value.format(str(e)))
		return result

	def initializeBootstrap(self):
		parser = Parser()
		self.interpret(parser.parse("'self_files/bootstrap.self' _RunScript."))
		self.interpret(parser.parse("'self_files/boolean.self' _RunScript."))