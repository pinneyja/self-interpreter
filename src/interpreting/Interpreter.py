from parsing.Parser import *
from interpreting.objects.SelfException import *
from parsing.SelfParsingError import *
from Messages import *

class Interpreter:
	def interpret(self, syntaxTree):
		try:
			result = syntaxTree.interpret(None)
		except (SelfException, SelfParsingError) as e:
			raise e
		except Exception as e:
			raise SelfException(Messages.GENERIC_ERROR.value.format(str(e)))
		return result