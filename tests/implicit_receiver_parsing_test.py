from parsing.Parser import *
from parsing.nodes.UnaryMessageNode import *

def test_basic_implicit_message_parsing():
	parser = Parser()

	message = "message"
	unary_message = UnaryMessageNode(None, message)
	parsed_message = parser.parse(message)

	assert str(unary_message) == str(parsed_message)