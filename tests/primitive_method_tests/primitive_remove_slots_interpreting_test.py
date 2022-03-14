from interpreting.Interpreter import Interpreter
from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.SelfObject import SelfObject

def test_basic_remove_slot():
	parser = Parser()
	interpreter = Interpreter()

	interpreted_result = interpreter.interpret(parser.parse("(|x = 1|) _RemoveSlot: 'x'"))
	expected_result = SelfObject()

	assert str(interpreted_result) == str(expected_result)

def test_basic_remove_parent_slot():
	parser = Parser()
	interpreter = Interpreter()

	interpreted_result = interpreter.interpret(parser.parse("(|p* = 1.|) _RemoveSlot: 'p'"))
	expected_result = SelfObject()

	assert str(interpreted_result) == str(expected_result)