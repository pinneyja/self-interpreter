from parsing.Parser import *

class Interpreter:
	def interpret(self, syntaxTree):
		return syntaxTree.interpret(None)