from parsing.nodes.DataSlotNode import *
from parsing.nodes.UnaryMessageNode import *
from parsing.nodes.ParentSlotNode import *
from parsing.nodes.CodeNode import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.IntegerNode import *
from parsing.Parser import *

def test_undirected_resend():
	parser = Parser()

	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("resend"), 'a')])))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([DataSlotNode('a', '=', IntegerNode(1))]))
	expected_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])

	parsed_node = parser.parse("(| p* = (|a = 1|). x = (| | resend.a) |) x")

	assert str(parsed_node) == str(expected_node)

	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([BinaryMessageNode(ResendNode("resend"), '+', IntegerNode(5))])))
	binary_slot = BinarySlotNode('+', RegularObjectNode(None, CodeNode([UnaryMessageNode(None, 'arg')])), 'arg')
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([binary_slot]))
	expected_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])

	parsed_node = parser.parse("(| p* = (| + arg = (| | arg) |). x = (| | resend.+5) |) x")

	assert str(parsed_node) == str(expected_node)

def test_directed_resend():
	parser = Parser()

	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("p"), 'a')])))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([DataSlotNode('a', '=', IntegerNode(1))]))
	expected_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])

	parsed_node = parser.parse("(| p* = (|a = 1|). x = (| | p.a) |) x")

	assert str(parsed_node) == str(expected_node)

	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([BinaryMessageNode(ResendNode("p"), '+', IntegerNode(5))])))
	binary_slot = BinarySlotNode('+', RegularObjectNode(None, CodeNode([UnaryMessageNode(None, 'arg')])), 'arg')
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([binary_slot]))
	expected_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])

	parsed_node = parser.parse("(| p* = (| + arg = (| | arg) |). x = (| | p.+5) |) x")

	assert str(parsed_node) == str(expected_node)