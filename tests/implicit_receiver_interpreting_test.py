from interpreting.Interpreter import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.UnaryMessageNode import *
from parsing.nodes.IntegerNode import *

def test_basic_valid_implicit_message_passing():
	pass # TODO: No way to test this until we have object permanence (aka lobby)

def test_implicit_message_passing_in_method_slot():
	# (| object1 = (| int1 = 1 | int1)|) object1
	interpreter = Interpreter()

	code = UnaryMessageNode(None, "int1")
	slot_list = [ DataSlotNode("int1", "=", IntegerNode(1)) ]
	reg_object = RegularObjectNode(slot_list, code)
	slot_list1 = [ DataSlotNode("object1", "=", reg_object)]
	reg_object1 = RegularObjectNode(slot_list1)
	unary_message = UnaryMessageNode(reg_object1, "object1")

	interpreted_result = interpreter.interpret(unary_message)

	assert str(interpreted_result) == str(SelfInteger(1))

def test_invalid_implicit_message_passing():
	# (| object1 = (| int1 = 1 | int2)|) object1
	interpreter = Interpreter()

	code = UnaryMessageNode(None, "int2")
	slot_list = [ DataSlotNode("int1", "=", IntegerNode(1)) ]
	reg_object = RegularObjectNode(slot_list, code)
	slot_list1 = [ DataSlotNode("object1", "=", reg_object)]
	reg_object1 = RegularObjectNode(slot_list1)
	unary_message = UnaryMessageNode(reg_object1, "object1")

	interpreted_result = interpreter.interpret(unary_message)

	assert str(interpreted_result) == str(SelfException("Lookup error: no matching slot"))

def test_implicit_binary_message_passing_in_method_slot():
	# (| object1 = (| + arg = (| | 1) | + 5)|) object1
	interpreter = Interpreter()

	code = BinaryMessageNode(None, "+", SelfInteger(5))
	slot_list = [ BinarySlotNode("+", IntegerNode(1), "arg") ]
	reg_object = RegularObjectNode(slot_list, code)
	slot_list1 = [ DataSlotNode("object1", "=", reg_object)]
	reg_object1 = RegularObjectNode(slot_list1)
	unary_message = UnaryMessageNode(reg_object1, "object1")

	interpreted_result = interpreter.interpret(unary_message)

	assert str(interpreted_result) == str(SelfInteger(1))