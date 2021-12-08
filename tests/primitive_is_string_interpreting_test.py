from parsing.Parser import Parser
from interpreting.Interpreter import Interpreter
from interpreting.objects.SelfString import SelfString
from interpreting.objects.SelfInteger import SelfInteger

def test_simple_string():
	parser = Parser()
	interpreter = Interpreter()

	result = interpreter.interpret(parser.parse("'testString' _IsStringIfFalse: [badMessage. 2. 3]"))
	assert str(result) == str(SelfString("testString"))

def test_non_strings():
	parser = Parser()
	interpreter = Interpreter()

	result = interpreter.interpret(parser.parse("123 _IsStringIfFalse: [1. 2. 3]"))
	assert str(result) == str(SelfInteger(3))

	result = interpreter.interpret(parser.parse("(| x <- 3 |) _IsStringIfFalse: [1. 2. 3]"))
	assert str(result) == str(SelfInteger(3))

	result = interpreter.interpret(parser.parse("() _IsStringIfFalse: [1. 2. 3]"))
	assert str(result) == str(SelfInteger(3))

	result = interpreter.interpret(parser.parse("[1. 2. 3] _IsStringIfFalse: [1. 2. 3]"))
	assert str(result) == str(SelfInteger(3))

def test_complicated_blocks():
	parser = Parser()
	interpreter = Interpreter()

	result = interpreter.interpret(parser.parse("123 _IsStringIfFalse: [lobby _AddSlots: (| x <-3 |). 2. 3. lobby x]"))
	assert str(result) == str(SelfInteger(3))

	result = interpreter.interpret(parser.parse("(| x <- 3 |) _IsStringIfFalse: [lobby _AddSlots: (| x <-2 |). x: 5. lobby x]"))
	assert str(result) == str(SelfInteger(5))

	result = interpreter.interpret(parser.parse("(| x <- 3 |) _IsStringIfFalse: [[^ 2] value. 9]"))
	assert str(result) == str(SelfInteger(2))