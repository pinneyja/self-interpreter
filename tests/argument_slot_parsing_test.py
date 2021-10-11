from parsing.Parser import *
from parsing.nodes.BinarySlotNode import *
from parsing.nodes.ArgumentSlotNode import *

def test_basic_argument_slot():
	# (| + = (|:arg| 5)|)
	parser = Parser()

	inner_reg_object = RegularObjectNode([ ArgumentSlotNode("arg") ], CodeNode([IntegerNode(5)]))
	reg_object = CodeNode([RegularObjectNode([ BinarySlotNode("+", inner_reg_object) ])])

	parsed_object = parser.parse("(| + = (|:arg| 5)|)")
	assert str(reg_object) == str(parsed_object)

	# (| + = (|:test| 5)|)
	inner_reg_object = RegularObjectNode([ ArgumentSlotNode("test") ], CodeNode([IntegerNode(5)]))
	reg_object = CodeNode([RegularObjectNode([ BinarySlotNode("+", inner_reg_object) ])])

	parsed_object = parser.parse("(| + = (|:test| 5)|)")
	assert str(reg_object) == str(parsed_object)

def test_argument_slot_in_list():
	# (| + = (|x. :arg| 5)|)
	parser = Parser()

	inner_reg_object = RegularObjectNode([ DataSlotNode("x"), ArgumentSlotNode("arg") ], CodeNode([IntegerNode(5)]))
	reg_object = CodeNode([RegularObjectNode([ BinarySlotNode("+", inner_reg_object) ])])

	parsed_object = parser.parse("(| + = (|x. :arg| 5)|)")
	assert str(reg_object) == str(parsed_object)