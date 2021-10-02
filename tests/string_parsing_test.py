import random
from parsing.Parser import *
from parsing.nodes.StringNode import *
from parsing.SelfParsingError import *
import pytest

def test_parse_simple_string():
	parser = Parser()

	node = StringNode('abcXYZ')
	parserNode = parser.parse('\'abcXYZ\'')

	generatedNodeString = str(node)
	parserNodeString = str(parserNode)
	assert generatedNodeString == parserNodeString

def test_parse_string_with_escape_characters():
	parser = Parser()

	node = StringNode('\t\b\n\f\r\v\a\0\\\'\"?')
	parserNode = parser.parse(r"'\t\b\n\f\r\v\a\0\\\'\"\?'")

	generatedNodeString = str(node)
	parserNodeString = str(parserNode)
	assert generatedNodeString == parserNodeString

def test_parse_string_with_numeric_escapes():
	parser = Parser()

	node = StringNode('abc\xff\xff\xff')
	parserNode = parser.parse(r"'\x61\d098\o143\xff\d255\o377'")

	generatedNodeString = str(node)
	parserNodeString = str(parserNode)
	assert generatedNodeString == parserNodeString

def test_parse_string_with_bad_escape_characters():
	parser = Parser()

	with pytest.raises(Exception) as e:
		parser.parse(r"'\p'")
	assert e.type == SelfParsingError

def test_parse_string_with_bad_numeric_escapes():
	parser = Parser()

	with pytest.raises(Exception) as e:
		parser.parse(r"'\o11'")
	assert e.type == SelfParsingError

	with pytest.raises(Exception) as e:
		parser.parse(r"'\o500'")
	assert e.type == SelfParsingError