from parsing.Parser import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.IntegerNode import *


def test_parse_object_with_only_code():
	parser = Parser()

	empty_object = CodeNode([RegularObjectNode([], CodeNode([RegularObjectNode([DataSlotNode("x", "=", IntegerNode(5))], None)]))])
	parsed_empty = parser.parse("(| |(|x=5|))")
	parsed_empty_pipe = parser.parse("(| | (|x=5|))")
	
	assert str(empty_object) == str(parsed_empty)
	assert str(empty_object) == str(parsed_empty_pipe)

def test_parse_object_with_code_and_slots():
	parser = Parser()

	obect_with_code_and_slots = CodeNode([RegularObjectNode([DataSlotNode("x", "<-", IntegerNode(1)), DataSlotNode("y")], CodeNode([IntegerNode(5)]))])

	parsed = parser.parse("(|x <- 1. y| 5)")

	assert str(parsed) == str(obect_with_code_and_slots)

def test_parse_object_with_code_inside_of_object_with_code():
	parser = Parser()

	object_with_nested_method_objects = CodeNode([RegularObjectNode([DataSlotNode("x","=",RegularObjectNode([], CodeNode([IntegerNode(1)])))], CodeNode([IntegerNode(2)]))])

	parsed = parser.parse("(|x=(| | 1)| 2)")

	assert str(parsed) == str(object_with_nested_method_objects)

def test_parse_object_with_keyword_method_slot():
	parser = Parser()

	reg_object1 = CodeNode([RegularObjectNode([ KeywordSlotNode(["x:", "Y:"], RegularObjectNode([], CodeNode([IntegerNode(5)])), ["x1", "y1"]) ])])
	parsed_object = parser.parse("(|x: x1 Y: y1 = (| | 5)|)")
	assert str(reg_object1) == str(parsed_object)