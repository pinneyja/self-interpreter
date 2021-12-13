from interpreting.Interpreter import Interpreter
from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger

def test_booleans_simple():
	interpreter = Interpreter()
	parser = Parser()

	expected = SelfBoolean(True)
	
	interpreter.initializeBootstrap()
	actual = interpreter.interpret(parser.parse("(true && false) not"))

	assert str(actual) == str(expected)

def test_booleans_conditionals():
	interpreter = Interpreter()
	parser = Parser()

	expected = SelfInteger(6)
	
	interpreter.initializeBootstrap()
	actual = interpreter.interpret(parser.parse("(true ifTrue: [1] False: [2]) + (false ifTrue: [3] False: [5])."))

	assert str(actual) == str(expected)

def test_booleans_conditionals_in_traits_boolean():
	interpreter = Interpreter()
	parser = Parser()

	expected = SelfInteger(5)
	
	interpreter.initializeBootstrap()
	actual = interpreter.interpret(parser.parse("(true ifFalse: [1] True: [2]) + (false ifFalse: [3] True: [5])."))

	assert str(actual) == str(expected)