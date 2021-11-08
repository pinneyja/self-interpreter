from parsing.Parser import *
from parsing.nodes.IntegerNode import *
from parsing.nodes.CodeNode import *

def test_basic_code_parsing():
	parser = Parser()
	code = CodeNode([IntegerNode(1), IntegerNode(2), IntegerNode(3)])
	code_with_return = CodeNode([IntegerNode(1), IntegerNode(2), IntegerNode(3)])
	code_with_return.set_has_caret(True)

	assert str(code) == str(parser.parse("1. 2. 3"))
	assert str(code_with_return) == str(parser.parse("1. 2. ^3"))
	assert str(code) == str(parser.parse("1. 2. 3."))