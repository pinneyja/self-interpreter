from parsing.nodes.object_nodes.RegularObjectNode import *
from parsing.nodes.slot_nodes.DataSlotNode import *
from parsing.nodes.object_nodes.IntegerNode import *
from interpreting.Interpreter import *


def test_empty_object():
	# ()
	interpreter = Interpreter()

	parser_result = CodeNode([RegularObjectNode()])
	expected_result = SelfObject()

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_simple_object():
	# (|x = 4|)
	interpreter = Interpreter()

	parser_result = CodeNode([RegularObjectNode([DataSlotNode("x", "=", IntegerNode(4))])])
	slot_list = {}
	slot_list["x"] = SelfSlot("x", SelfInteger(4), is_immutable=True)
	expected_result = SelfObject(slot_list)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_complicated_object():
	# (|x = 4. y <- (|z = 4|)|)
	interpreter = Interpreter()

	parser_result = CodeNode([RegularObjectNode([DataSlotNode("x", "=", IntegerNode(4)), DataSlotNode("y", "<-", RegularObjectNode([DataSlotNode("z", "=", IntegerNode(4))]))])])
	slot_list = {}
	slot_list["x"] = SelfSlot("x", SelfInteger(4), is_immutable=True)
	inner_slot_list = {}
	inner_slot_list["z"] = SelfSlot("z", SelfInteger(4), is_immutable=True)
	slot_list["y"] = SelfSlot("y", SelfObject(inner_slot_list), is_immutable=False)
	
	arg_slots = OrderedDict()
	arg_slots["arg"] = SelfSlot("arg")
	code = KeywordMessageNode(None, ["_Assignment:", "Value:"], [StringNode("y"), UnaryMessageNode(None, "arg")])
	slot_list["y:"] = SelfSlot("y:", SelfObject(arg_slots=arg_slots, code=code), keyword_list=["y:"])
	
	expected_result = SelfObject(slot_list)
	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)
