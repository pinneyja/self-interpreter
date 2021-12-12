from parsing.nodes.object_nodes.RegularObjectNode import *
from parsing.nodes.slot_nodes.DataSlotNode import *
from parsing.nodes.slot_nodes.BinarySlotNode import *
from parsing.nodes.object_nodes.IntegerNode import *
from parsing.nodes.message_nodes.UnaryMessageNode import *
from interpreting.Interpreter import *

def test_basic_binary_message_passing():
	# (| + = (|:arg| arg)|) + 5
	interpreter = Interpreter()

	reg_object = RegularObjectNode([ BinarySlotNode("+", RegularObjectNode([ArgumentSlotNode("arg")], CodeNode([UnaryMessageNode(None, "arg")]))) ])
	parser_result = CodeNode([BinaryMessageNode(reg_object, "+", IntegerNode(5))])
	interpreted_result = interpreter.interpret(parser_result)

	expected_result = SelfInteger(5)

	assert str(interpreted_result) == str(expected_result)

def test_basic_binary_message_passing_with_syntactic_sugar():
	# (| + arg = (| | arg)|) + 5
	interpreter = Interpreter()

	reg_object = RegularObjectNode([ BinarySlotNode("+", RegularObjectNode(code=CodeNode([UnaryMessageNode(None, "arg")])), "arg") ])
	parser_result = CodeNode([BinaryMessageNode(reg_object, "+", IntegerNode(5))])
	interpreted_result = interpreter.interpret(parser_result)

	expected_result = SelfInteger(5)

	assert str(interpreted_result) == str(expected_result)

def test_operators_with_other_meanings():
	# (| <- = (|:arg| arg)|) <- 5
	interpreter = Interpreter()

	reg_object = RegularObjectNode([ DataSlotNode("<-", "=", RegularObjectNode([ArgumentSlotNode("arg")], CodeNode([UnaryMessageNode(None, "arg")]))) ])
	parser_result = CodeNode([BinaryMessageNode(reg_object, "<-", IntegerNode(5))])
	interpreted_result_larrow = interpreter.interpret(parser_result)

	# (| = = (|:arg| arg)|) = 5
	reg_object = RegularObjectNode([ DataSlotNode("=", "=", RegularObjectNode([ArgumentSlotNode("arg")], CodeNode([UnaryMessageNode(None, "arg")]))) ])
	parser_result = CodeNode([BinaryMessageNode(reg_object, "=", IntegerNode(5))])
	interpreted_result_equal = interpreter.interpret(parser_result)

	expected_result = SelfInteger(5)

	assert str(interpreted_result_larrow) == str(expected_result)
	assert str(interpreted_result_equal) == str(expected_result)

def test_operators_with_other_meanings_syntactic_sugar():
	# (| <- arg = (| | arg)|) <- 5
	interpreter = Interpreter()

	reg_object = RegularObjectNode([ BinarySlotNode("<-", RegularObjectNode(code=CodeNode([UnaryMessageNode(None, "arg")])), "arg") ])
	parser_result = CodeNode([BinaryMessageNode(reg_object, "<-", IntegerNode(5))])
	interpreted_result_larrow = interpreter.interpret(parser_result)

	# (| = arg = (| | arg)|) = 5
	reg_object = RegularObjectNode([ BinarySlotNode("=", RegularObjectNode(code=CodeNode([UnaryMessageNode(None, "arg")])), "arg") ])
	parser_result = CodeNode([BinaryMessageNode(reg_object, "=", IntegerNode(5))])
	interpreted_result_equal = interpreter.interpret(parser_result)
	
	expected_result = SelfInteger(5)

	assert str(interpreted_result_larrow) == str(expected_result)
	assert str(interpreted_result_equal) == str(expected_result)