from parsing.Parser import *
from parsing.nodes.slot_nodes.ParentSlotNode import *

def test_basic_parent_slot():
	parser = Parser()

	inner_reg_object = RegularObjectNode()
	reg_object = CodeNode([RegularObjectNode([ ParentSlotNode("parent", "=", inner_reg_object) ])])

	parsed_object = parser.parse("(| parent* = (| |) |)")
	assert str(reg_object) == str(parsed_object)

def test_nested_parent_slots():
	parser = Parser()

	inner_reg_object = RegularObjectNode([ ParentSlotNode("parent2", "=", RegularObjectNode()) ])
	reg_object = CodeNode([RegularObjectNode([ ParentSlotNode("parent", "=", inner_reg_object) ])])

	parsed_object = parser.parse("(| parent* = (| parent2* = (| |) |) |)")
	assert str(reg_object) == str(parsed_object)

def test_multiple_parent_slots():
	parser = Parser()

	reg_object = CodeNode([RegularObjectNode([ ParentSlotNode("parent", "=", RegularObjectNode()), ParentSlotNode("parent2", "=", IntegerNode(5)) ])])

	parsed_object = parser.parse("(| parent* = (| |). parent2* = 5 |)")
	assert str(reg_object) == str(parsed_object)