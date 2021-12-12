from parsing.Parser import *
from parsing.nodes.object_nodes.RegularObjectNode import *
from parsing.nodes.slot_nodes.DataSlotNode import *
from parsing.nodes.object_nodes.IntegerNode import *


def test_parses_empty_object():
	parser = Parser()

	empty_object = CodeNode([RegularObjectNode()])
	parsed_empty = parser.parse("()")
	parsed_empty_pipe = parser.parse("(| |)")
	
	assert str(empty_object) == str(parsed_empty)
	assert str(empty_object) == str(parsed_empty_pipe)

def test_parses_one_number_slot():
	parser = Parser()

	one_slot_obj = CodeNode([RegularObjectNode([DataSlotNode("x")])])
	one_slot_obj_equal = CodeNode([RegularObjectNode([DataSlotNode("x","=",IntegerNode(5))])])
	one_slot_obj_larrow = CodeNode([RegularObjectNode([DataSlotNode("x","<-",IntegerNode(5))])])

	parsed_one_slot_obj = parser.parse("(|x|)")
	parsed_one_slot_obj_dot = parser.parse("(|x. |)")
	parsed_one_slot_obj_equal = parser.parse("(|x=5|)")
	parsed_one_slot_obj_equal_dot = parser.parse("(|x=5.|)")
	parsed_one_slot_obj_larrow = parser.parse("(|x<-5|)")
	parsed_one_slot_obj_larrow_dot = parser.parse("(|x<-5.|)")

	assert str(parsed_one_slot_obj) == str(one_slot_obj)
	assert str(parsed_one_slot_obj_dot) == str(one_slot_obj)
	assert str(parsed_one_slot_obj_equal) == str(one_slot_obj_equal)
	assert str(parsed_one_slot_obj_equal_dot) == str(one_slot_obj_equal)
	assert str(parsed_one_slot_obj_larrow) == str(one_slot_obj_larrow)
	assert str(parsed_one_slot_obj_larrow_dot) == str(one_slot_obj_larrow)

def test_parses_multiple_number_slot():
	parser = Parser()

	slot_obj_equal = CodeNode([RegularObjectNode([DataSlotNode("x","=",IntegerNode(5)), DataSlotNode("y","=",IntegerNode(6))])])
	slot_obj_larrow = CodeNode([RegularObjectNode([DataSlotNode("x","<-",IntegerNode(5)), DataSlotNode("y","<-",IntegerNode(6))])])

	parsed_slot_obj_equal = parser.parse("(|x=5.y=6.|)")
	parsed_slot_obj_larrow = parser.parse("(|x<-5. y<-6|)")

	assert str(parsed_slot_obj_equal) == str(slot_obj_equal)
	assert str(parsed_slot_obj_larrow) == str(slot_obj_larrow)

def test_nested_object_slot():
	parser = Parser()

	slot_obj_equal_empty = CodeNode([RegularObjectNode([DataSlotNode("x","=",RegularObjectNode())])])
	slot_obj_larrow_nested = CodeNode([RegularObjectNode([DataSlotNode("y","<-",RegularObjectNode([DataSlotNode("x","=",IntegerNode(5)), DataSlotNode("z","=",IntegerNode(6))]))])])

	parsed_slot_obj_equal_empty = parser.parse("(|x=()|)")
	parsed_slot_obj_larrow_nested = parser.parse("(|y<-(|x=5. z=6|)|)")

	assert str(slot_obj_equal_empty) == str(parsed_slot_obj_equal_empty)
	assert str(slot_obj_larrow_nested) == str(parsed_slot_obj_larrow_nested)