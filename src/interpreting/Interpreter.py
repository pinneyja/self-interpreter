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
		activation_object = SelfObject()
		activation_object.parent_slots["self"] = SelfSlot("self", self.lobby, True)
		result = syntaxTree.interpret(activation_object)
		return result

	def initializeBootstrap(self):
		parser = Parser()
		files_to_load = ["bootstrap", "rootTraits", "nil", "boolean", "block", "smallInt", "integer", "defaultBehavior", "integerIteration", "number", "collector", "collection", "list", "vector", "indexable", "string", "float", "setAndDictionary", "canvas"]

		for file_name in files_to_load:
			self.interpret(parser.parse(f"'self_files/{file_name}.self' _RunScript."))

		self.interpret(parser.parse("traits string initializeAscii"))
