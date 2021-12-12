from parsing.Parser import *
from parsing.nodes.message_nodes.UnaryMessageNode import *
from parsing.nodes.message_nodes.BinaryMessageNode import *

def test_basic_implicit_unary_message_parsing():
	parser = Parser()

	message = "message"
	unary_message = CodeNode([UnaryMessageNode(None, message)])
	parsed_message = parser.parse(message)

	assert str(unary_message) == str(parsed_message)

def test_basic_implicit_binary_message_parsing():
	parser = Parser()

	message = "+ 5"
	binary_message = CodeNode([BinaryMessageNode(None, "+", IntegerNode(5))])
	parsed_message = parser.parse(message)

	assert str(binary_message) == str(parsed_message)

def test_basic_implicit_keyword_message_parsing():
	parser = Parser()

	binary_message = CodeNode([KeywordMessageNode(None, ["x:", "Y:"], [IntegerNode(1), RegularObjectNode()])])
	parsed_object = parser.parse("x: 1 Y: ()")
	assert str(binary_message) == str(parsed_object)
	