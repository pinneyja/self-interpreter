from parsing.Parser import *
from parsing.nodes.IntegerNode import *

def test_basic_keyword_message_parsing():
	parser = Parser()

	keyword_message = KeywordMessageNode(IntegerNode(1), ["x:", "Y:"], [IntegerNode(1), RegularObjectNode()])
	parsed_object = parser.parse("1 x: 1 Y: ()")
	assert str(keyword_message) == str(parsed_object)

#TODO: (for team) Add as many distinct useful tests of ambiguity handling as possible
def test_keyword_message_ambiguity_chained_message():
	parser = Parser()

	keyword_message_1 = KeywordMessageNode(RegularObjectNode(), ["z:", "A:"], [IntegerNode(2), IntegerNode(5)])
	keyword_message = KeywordMessageNode(IntegerNode(1), ["x:", "Y:"], [IntegerNode(1), keyword_message_1])
	parsed_object = parser.parse("1 x: 1 Y: () z: 2 A: 5")
	assert str(keyword_message) == str(parsed_object)

def test_keyword_message_ambiguity_chained_binary_message():
	parser = Parser()

	binary_message_2 = BinaryMessageNode(IntegerNode(1), "+", IntegerNode(2))
	keyword_message_1 = KeywordMessageNode(binary_message_2, ["z:", "A:"], [RegularObjectNode(), IntegerNode(5)])
	keyword_message = KeywordMessageNode(IntegerNode(1), ["x:", "Y:"], [IntegerNode(1), keyword_message_1])
	parsed_object = parser.parse("1 x: 1 Y: 1 + 2 z: () A: 5")
	assert str(keyword_message) == str(parsed_object)

def test_keyword_message_precedence_chained_binary_message():
	parser = Parser()

	binary_message_3 = BinaryMessageNode(IntegerNode(1), "+", IntegerNode(2))
	keyword_message_2 = KeywordMessageNode(binary_message_3, ["a:"], [IntegerNode(5)])
	keyword_message_1 = KeywordMessageNode(RegularObjectNode(), ["z:"], [keyword_message_2])
	keyword_message = KeywordMessageNode(IntegerNode(1), ["x:", "Y:"], [IntegerNode(1), keyword_message_1])
	parsed_object = parser.parse("1 x: 1 Y: () z: 1 + 2 a: 5")
	assert str(keyword_message) == str(parsed_object)