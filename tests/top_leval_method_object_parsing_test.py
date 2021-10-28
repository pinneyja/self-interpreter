from parsing.Parser import *
import pytest


def test_parse_simple_top_level_method():
	parser = Parser()

	node = CodeNode([BinaryMessageNode(IntegerNode(1), "+", IntegerNode(2))])
	parsed = parser.parse("(| | 1 + 2)")
	
	assert str(node) == str(parsed)

def test_parse_top_level_in_code():
	parser = Parser()

	node = CodeNode([UnaryMessageNode(None, "badMessage"), BinaryMessageNode(IntegerNode(2), "+", IntegerNode(3))])
	parsed = parser.parse("(| | badMessage). (| | 2 + 3)")
	
	assert str(node) == str(parsed)

def test_parse_throws_multiple_expressions_in_sub_expression():
	parser = Parser()

	with pytest.raises(SelfParsingError, match=Messages.MULTIPLE_EXPRESSIONS_IN_SUB_EXPRESSION.value):
		parsed = parser.parse("(| | 1. 2)")