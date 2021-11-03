from parsing.nodes.IntegerNode import *
from parsing.nodes.StringNode import *
from parsing.nodes.KeywordMessageNode import *
from interpreting.Interpreter import *


def test_empty_assignment():
	# ((| x |) x: 2) x
	interpreter = Interpreter()

	original_object = RegularObjectNode(slot_list=[DataSlotNode("x")])
	keyword_message = KeywordMessageNode(original_object, ["x:"], [IntegerNode(2)])
	unary_message = UnaryMessageNode(keyword_message, "x")
	parser_result = CodeNode([unary_message])
	
	expected_result = SelfInteger(2)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_simple_assignment():
	# ((| x <- 1 |) x: 2) x
	interpreter = Interpreter()

	original_object = RegularObjectNode(slot_list=[DataSlotNode("x", "<-", IntegerNode(1))])
	keyword_message = KeywordMessageNode(original_object, ["x:"], [IntegerNode(2)])
	unary_message = UnaryMessageNode(keyword_message, "x")
	parser_result = CodeNode([unary_message])
	
	expected_result = SelfInteger(2)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_simple_assignment_in_code():
	# (| m = (| x <- 1| x: 2) |) m x
	interpreter = Interpreter()

	keyword_message = KeywordMessageNode(None, ["x:"], [IntegerNode(2)])
	inner_regular_object = RegularObjectNode(slot_list=[DataSlotNode("x", "<-", IntegerNode(1))], code=CodeNode([keyword_message]))
	regular_object = RegularObjectNode(slot_list=[DataSlotNode("m", "=", inner_regular_object)])
	inner_unary_message = UnaryMessageNode(regular_object, "m")
	unary_message = UnaryMessageNode(inner_unary_message, "x")
	parser_result = CodeNode([unary_message])
	
	expected_result = SelfInteger(2)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_simple_parent_assignment():
	# ((| x* <- 1 |) x: 2) x
	interpreter = Interpreter()

	original_object = RegularObjectNode(slot_list=[ParentSlotNode("x", "<-", IntegerNode(1))])
	keyword_message = KeywordMessageNode(original_object, ["x:"], [IntegerNode(2)])
	unary_message = UnaryMessageNode(keyword_message, "x")
	parser_result = CodeNode([unary_message])
	
	expected_result = SelfInteger(2)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_more_complex_assignment():
	# (((| x <- 1 |) x: (| a = 6. b = 2|))) x) a
	# (((| x <- 1 |) x: (| a = 6. b = 2|))) x) b
	interpreter = Interpreter()

	original_object = RegularObjectNode(slot_list=[DataSlotNode("x", "<-", IntegerNode(1))])
	new_assignment = RegularObjectNode([DataSlotNode("a", "=", IntegerNode(6)), DataSlotNode("b", "=", IntegerNode(2))])
	keyword_message = KeywordMessageNode(original_object, ["x:"], [new_assignment])
	unary_message = UnaryMessageNode(keyword_message, "x")
	unary_message_a = UnaryMessageNode(unary_message, "a")
	unary_message_b = UnaryMessageNode(unary_message, "b")
	parser_result_a = CodeNode([unary_message_a])
	parser_result_b = CodeNode([unary_message_b])
	
	expected_result_a = SelfInteger(6)
	expected_result_b = SelfInteger(2)

	interpreted_result_a = interpreter.interpret(parser_result_a)
	interpreted_result_b = interpreter.interpret(parser_result_b)

	assert str(interpreted_result_a) == str(expected_result_a)
	assert str(interpreted_result_b) == str(expected_result_b)

def test_does_not_assign_equals():
	# ((| x = 1 |) x: 2) x
	interpreter = Interpreter()

	original_object = RegularObjectNode(slot_list=[DataSlotNode("x", "=", IntegerNode(1))])
	keyword_message = KeywordMessageNode(original_object, ["x:"], [IntegerNode(2)])
	unary_message = UnaryMessageNode(keyword_message, "x")
	parser_result = CodeNode([unary_message])
	
	expected_result = SelfInteger(2)

	try:
		interpreted_result = interpreter.interpret(parser_result)
		assert False
	except SelfException as selfException:
		assert str(selfException) == str(SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value.format("x:")))

def test_simple_parent_assignment():
	# ((| p* = (| x <- 1 |) |) x: 2) x
	interpreter = Interpreter()

	parent_object = RegularObjectNode(slot_list=[DataSlotNode("x", "<-", IntegerNode(1))])
	original_object = RegularObjectNode(slot_list=[ParentSlotNode("p", "<-", parent_object)])
	keyword_message = KeywordMessageNode(original_object, ["x:"], [IntegerNode(2)])
	unary_message = UnaryMessageNode(keyword_message, "x")
	parser_result = CodeNode([unary_message])
	
	expected_result = SelfInteger(2)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_does_not_assign_equals_primitive():
	# ((| x = 1 |) _Assignment: 'x' Value: 2) x
	interpreter = Interpreter()

	original_object = RegularObjectNode(slot_list=[DataSlotNode("x", "=", IntegerNode(1))])
	keyword_message = KeywordMessageNode(original_object, ["_Assignment:", "Value:"], [StringNode("x"), IntegerNode(2)])
	unary_message = UnaryMessageNode(keyword_message, "x")
	parser_result = CodeNode([unary_message])
	
	expected_result = SelfInteger(2)

	try:
		interpreted_result = interpreter.interpret(parser_result)
		assert False
	except SelfException as selfException:
		assert str(selfException) == str(SelfException(Messages.LOOKUP_ERROR_NO_SLOT.value.format("x:")))