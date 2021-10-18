from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.IntegerNode import *
from parsing.nodes.UnaryMessageNode import *
from interpreting.Interpreter import *
from Messages import *

def test_simply_unary_method_call():
	# (|x = (| | 1)|) x
	interpreter = Interpreter()

	parser_result = CodeNode([UnaryMessageNode(RegularObjectNode([DataSlotNode("x","=",RegularObjectNode([], IntegerNode(1)))]), "x")])
	expected_result = SelfInteger(1)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_method_code_is_not_run_until_called():
	# (|x = (| | () bogus)|)
	interpreter = Interpreter()

	parser_result = CodeNode([RegularObjectNode([DataSlotNode("x","=",RegularObjectNode([], UnaryMessageNode(RegularObjectNode(), "bogus")))])])
	slot_list = {}
	self_object_inner = SelfObject(code=UnaryMessageNode(RegularObjectNode(), "bogus"))
	slot_list["x"] = SelfSlot("x", self_object_inner, isImmutable=True)
	expected_result = SelfObject(slot_list)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_method_code_with_bad_unary_message():
	# (|x = (| | () bogus)|) x
	interpreter = Interpreter()

	parser_result_object = RegularObjectNode([DataSlotNode("x","=",RegularObjectNode([], UnaryMessageNode(RegularObjectNode(), "bogus")))])
	parser_result = CodeNode([UnaryMessageNode(parser_result_object, "x")])

	try:
		interpreted_result = interpreter.interpret(parser_result)
		assert False
	except SelfException as selfException:
		assert str(selfException) == Messages.LOOKUP_ERROR_NO_SLOT.value

def test_method_code_parent_lookup():
	# (|y = 5. x = (| | y)|) x
	interpreter = Interpreter()

	parser_result_object = RegularObjectNode([DataSlotNode("y", "=", IntegerNode(5)), DataSlotNode("x","=",RegularObjectNode([], CodeNode([UnaryMessageNode(None, "y")])))])
	parser_result = CodeNode([UnaryMessageNode(parser_result_object, "x")])
	expected_result = SelfInteger(5)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_method_code_parent_lookup_using_self_slot():
	# (|y = 5. x = (| | self y)|) x
	interpreter = Interpreter()

	code = CodeNode([UnaryMessageNode(UnaryMessageNode(None, "self"), "y")])
	parser_result_object = RegularObjectNode([DataSlotNode("y", "=", IntegerNode(5)), DataSlotNode("x","=",RegularObjectNode([], code))])
	parser_result = CodeNode([UnaryMessageNode(parser_result_object, "x")])
	expected_result = SelfInteger(5)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)