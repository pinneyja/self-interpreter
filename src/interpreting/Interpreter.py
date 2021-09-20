from interpreting.Environment import *
from parsing.Parser import *

class Interpreter:	
	
	@staticmethod
	def createInitialEnvironment():
		return Environment()

	def __init__(self, initialEnvironment = None):
		self.environment = initialEnvironment
		if(not self.environment):
			self.environment = Interpreter.createInitialEnvironment()

	def interpret(self, syntaxTree):
		return syntaxTree.interpret(self.environment)