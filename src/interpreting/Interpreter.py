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
			activation_object = SelfObject()
			activation_object.parent_slots["self"] = SelfSlot("self", self.lobby, True)
			result = syntaxTree.interpret(activation_object)
		except (SelfException, SelfParsingError) as e:
			raise e
		# except Exception as e:
		# 	raise SelfException(Messages.GENERIC_ERROR.value.format(str(e)))
		return result

	def initializeBootstrap(self):
		parser = Parser()
		self.interpret(parser.parse("'self_files/bootstrap.self' _RunScript."))
		self.interpret(parser.parse("'self_files/rootTraits.self' _RunScript."))
		self.interpret(parser.parse("'self_files/nil.self' _RunScript."))
		self.interpret(parser.parse("'self_files/boolean.self' _RunScript."))
		self.interpret(parser.parse("'self_files/block.self' _RunScript."))
		self.interpret(parser.parse("'self_files/smallInt.self' _RunScript."))
		self.interpret(parser.parse("'self_files/integer.self' _RunScript."))
		self.interpret(parser.parse("'self_files/defaultBehavior.self' _RunScript."))
		self.interpret(parser.parse("'self_files/integerIteration.self' _RunScript."))
		self.interpret(parser.parse("'self_files/float.self' _RunScript."))
		self.interpret(parser.parse("'self_files/number.self' _RunScript."))
		self.interpret(parser.parse("'self_files/collector.self' _RunScript."))
		self.interpret(parser.parse("'self_files/collection.self' _RunScript."))
		self.interpret(parser.parse("'self_files/list.self' _RunScript."))
		self.interpret(parser.parse("'self_files/vector.self' _RunScript."))
		self.interpret(parser.parse("'self_files/indexable.self' _RunScript."))
