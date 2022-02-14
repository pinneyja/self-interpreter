from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger

def test_booleans_simple(interpreter):
	parser = Parser()

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("(true && false) not"))

	assert str(actual) == str(expected)

def test_booleans_conditionals(interpreter):
	parser = Parser()

	expected = SelfInteger(6)
	actual = interpreter.interpret(parser.parse("(true ifTrue: [1] False: [2]) + (false ifTrue: [3] False: [5])."))

	assert str(actual) == str(expected)

def test_booleans_conditionals_in_traits_boolean(interpreter):
	parser = Parser()

	expected = SelfInteger(5)
	actual = interpreter.interpret(parser.parse("(true ifFalse: [1] True: [2]) + (false ifFalse: [3] True: [5])."))

	assert str(actual) == str(expected)