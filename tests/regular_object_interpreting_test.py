from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.IntegerNode import *
from interpreting.Environment import *
from interpreting.Interpreter import *


def test_empty_object():
	interpreter = Interpreter()

	environment = Environment()
	parser_result = RegularObjectNode()
	expected_result = SelfObject()

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_simple_object():
	interpreter = Interpreter()

	environment = Environment()
	parser_result = RegularObjectNode([DataSlotNode("x", "=", IntegerNode(4))])
	slot_list = {}
	slot_list["x"] = SelfSlot("x", SelfInteger('4'), isImmutable=True)
	expected_result = SelfObject(slot_list)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_complicated_object():
	interpreter = Interpreter()

	environment = Environment()
	parser_result = RegularObjectNode([DataSlotNode("x", "=", IntegerNode(4)), DataSlotNode("y", "<-", RegularObjectNode([DataSlotNode("z", "=", IntegerNode(4))]))])
	slot_list = {}
	slot_list["x"] = SelfSlot("x", SelfInteger('4'), isImmutable=True)
	inner_slot_list = {}
	inner_slot_list["z"] = SelfSlot("z", SelfInteger('4'), isImmutable=True)
	slot_list["y"] = SelfSlot("y", SelfObject(inner_slot_list), isImmutable=False)
	expected_result = SelfObject(slot_list)
	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)
