from interpreting.Interpreter import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.UnaryMessageNode import *
from parsing.nodes.IntegerNode import *

def test_basic_valid_unary_message_passing():
	# (|slot1 = 1. slot2 = 2|) slot1/slot2
	interpreter = Interpreter()

	slot_list = [ DataSlotNode("slot1", "=", IntegerNode(1)), DataSlotNode("slot2", "=", IntegerNode(2)) ]
	reg_object = RegularObjectNode(slot_list)
	unary_message_1 = UnaryMessageNode(reg_object, "slot1")
	unary_message_2 = UnaryMessageNode(reg_object, "slot2")

	interpreted_result_1 = interpreter.interpret(unary_message_1)
	interpreted_result_2 = interpreter.interpret(unary_message_2)

	assert str(interpreted_result_1) == str(SelfInteger(1))
	assert str(interpreted_result_2) == str(SelfInteger(2))

def test_nested_valid_unary_message_passing():
	# (|object1 = (|int1 = 1|)|) object1 int1
	interpreter = Interpreter()

	slot_list = [ DataSlotNode("int1", "=", IntegerNode(1)) ]
	reg_object = RegularObjectNode(slot_list)
	slot_list1 = [ DataSlotNode("object1", "=", reg_object)]
	reg_object1 = RegularObjectNode(slot_list1)
	unary_message1 = UnaryMessageNode(reg_object1, "object1")
	unary_message = UnaryMessageNode(unary_message1, "int1")

	interpreted_result = interpreter.interpret(unary_message)

	assert str(interpreted_result) == str(SelfInteger(1))

def test_invalid_unary_message_passing():
	# (|slot1 = 1|) slot1/slot2
	interpreter = Interpreter()

	slot_list = [ DataSlotNode("slot1", "=", IntegerNode(1)) ]
	reg_object = RegularObjectNode(slot_list)
	unary_message_1 = UnaryMessageNode(reg_object, "slot1")
	unary_message_2 = UnaryMessageNode(reg_object, "slot2")

	interpreted_result_1 = interpreter.interpret(unary_message_1)
	interpreted_result_2 = interpreter.interpret(unary_message_2)

	assert str(interpreted_result_1) == str(SelfInteger(1))
	assert str(interpreted_result_2) == str(SelfException("Lookup error"))