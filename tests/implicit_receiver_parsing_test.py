from parsing.Parser import *
from parsing.nodes.UnaryMessageNode import *
from parsing.nodes.BinaryMessageNode import *

def test_basic_implicit_unary_message_parsing():
	parser = Parser()

	message = "message"
	unary_message = UnaryMessageNode(None, message)
	parsed_message = parser.parse(message)

	assert str(unary_message) == str(parsed_message)

def test_basic_implicit_binary_message_parsing():
	parser = Parser()

	message = "+ 5"
	binary_message = BinaryMessageNode(None, "+", IntegerNode(5))
	parsed_message = parser.parse(message)

	assert str(binary_message) == str(parsed_message)