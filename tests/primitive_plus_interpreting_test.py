from parsing.nodes.IntegerNode import *
from parsing.nodes.BinaryMessageNode import *
from parsing.nodes.KeywordMessageNode import *
from interpreting.objects.SelfInteger import *
from interpreting.objects.SelfSlot import *
from interpreting.Interpreter import *


def test_simple_addition():
	# 1 + 3
	interpreter = Interpreter()

	parser_result = BinaryMessageNode(IntegerNode(1), "+", IntegerNode(3))
	expected_result = SelfInteger(4)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_multiple_addition():
	# 1 + 3 + 5
	interpreter = Interpreter()

	parser_result = BinaryMessageNode(BinaryMessageNode(IntegerNode(1), "+", IntegerNode(3)), "+", IntegerNode(5))
	expected_result = SelfInteger(9)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_primitive_addition():
	# 1 _IntAdd: 3
	interpreter = Interpreter()

	parser_result = KeywordMessageNode(IntegerNode(1), ["_IntAdd:"], [IntegerNode(3)])
	expected_result = SelfInteger(4)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_multiple_primitive_addition():
	# 1 _IntAdd: 3 _IntAdd: 5
	interpreter = Interpreter()

	parser_result = KeywordMessageNode(KeywordMessageNode(IntegerNode(1), ["_IntAdd:"], [IntegerNode(3)]), ["_IntAdd:"], [IntegerNode(5)])
	expected_result = SelfInteger(9)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)