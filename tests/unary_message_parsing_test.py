from parsing.Parser import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.UnaryMessageNode import *
from parsing.nodes.IntegerNode import *
from parsing.nodes.DataSlotNode import *

def test_basic_unary_message_parsing():
	parser = Parser()

	slot_list = [ DataSlotNode("slot1", "=", IntegerNode(1)) ]
	reg_object = RegularObjectNode(slot_list)
	unary_message = UnaryMessageNode(reg_object, "slot1")
	code = CodeNode([unary_message])

	parsed_object = parser.parse("(|slot1=1|) slot1")

	assert str(code) == str(parsed_object)

def test_nested_unary_message_parsing():
	parser = Parser()
	slot_list = [ DataSlotNode("int1", "=", IntegerNode(1)) ]
	reg_object = RegularObjectNode(slot_list)
	slot_list1 = [ DataSlotNode("object1", "=", reg_object)]
	reg_object1 = RegularObjectNode(slot_list1)
	unary_message1 = UnaryMessageNode(reg_object1, "object1")
	unary_message = UnaryMessageNode(unary_message1, "int1")
	code = CodeNode([unary_message])

	parsed_object = parser.parse("(|object1=(|int1=1|)|) object1 int1")

	assert str(code) == str(parsed_object)

