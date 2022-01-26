from parsing.nodes.object_nodes.IntegerNode import *
from parsing.nodes.message_nodes.BinaryMessageNode import *
from parsing.nodes.message_nodes.KeywordMessageNode import *
from interpreting.objects.primitive_objects.SelfInteger import *
from interpreting.objects.SelfSlot import *
from interpreting.Interpreter import *
from parsing.utils.SelfSnippets import addPlusString

def test_simple_addition():
	# 1 + 3
	interpreter = Interpreter()
	parser = Parser()
	interpreter.interpret(parser.parse(addPlusString))

	parser_result = CodeNode([BinaryMessageNode(IntegerNode(1), "+", IntegerNode(3))])
	expected_result = SelfInteger(4)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_multiple_addition():
	# 1 + 3 + 5
	interpreter = Interpreter()
	parser = Parser()
	interpreter.interpret(parser.parse(addPlusString))

	parser_result = CodeNode([BinaryMessageNode(BinaryMessageNode(IntegerNode(1), "+", IntegerNode(3)), "+", IntegerNode(5))])
	expected_result = SelfInteger(9)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_primitive_addition():
	# 1 _IntAdd: 3
	interpreter = Interpreter()

	parser_result = CodeNode([KeywordMessageNode(IntegerNode(1), ["_IntAdd:"], [IntegerNode(3)])])
	expected_result = SelfInteger(4)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_multiple_primitive_addition():
	# 1 _IntAdd: 3 _IntAdd: 5
	interpreter = Interpreter()

	parser_result = CodeNode([KeywordMessageNode(KeywordMessageNode(IntegerNode(1), ["_IntAdd:"], [IntegerNode(3)]), ["_IntAdd:"], [IntegerNode(5)])])
	expected_result = SelfInteger(9)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)