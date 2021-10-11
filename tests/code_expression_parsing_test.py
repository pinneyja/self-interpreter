from parsing.Parser import *
from parsing.nodes.IntegerNode import *
from parsing.nodes.CodeNode import *

def test_basic_code_parsing():
	parser = Parser()
	code = CodeNode([IntegerNode(1), IntegerNode(2), IntegerNode(3)])

	assert str(code) == str(parser.parse("1. 2. 3"))
	assert str(code) == str(parser.parse("1. 2. ^3"))
	assert str(code) == str(parser.parse("1. 2. 3."))