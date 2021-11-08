from parsing.Parser import Parser
from parsing.nodes.ArgumentSlotNode import ArgumentSlotNode
from parsing.nodes.CodeNode import CodeNode
from parsing.nodes.BlockNode import BlockNode
from parsing.nodes.DataSlotNode import DataSlotNode
from parsing.nodes.IntegerNode import IntegerNode
from parsing.nodes.ParentSlotNode import ParentSlotNode

def test_parses_empty_block():
	parser = Parser()

	empty_block = CodeNode([BlockNode()])
	parsed_empty = parser.parse("[]")
	parsed_empty_pipe = parser.parse("[]")
	
	assert str(empty_block) == str(parsed_empty)
	assert str(empty_block) == str(parsed_empty_pipe)

def test_parses_code_block():
	parser = Parser()

	code_block = CodeNode([BlockNode(code=CodeNode([IntegerNode(1), IntegerNode(2)]))])
	parsed_code = parser.parse("[1. 2]")
	parsed_code_pipe = parser.parse("[| | 1. 2]")
	
	assert str(code_block) == str(parsed_code)
	assert str(code_block) == str(parsed_code_pipe)

def test_parses_code_block_with_return():
	parser = Parser()

	inner_code_block = CodeNode([IntegerNode(1), IntegerNode(2)])
	inner_code_block.set_has_caret(True)

	code_block = CodeNode([BlockNode(code=inner_code_block)])
	parsed_code = parser.parse("[1. ^2]")
	parsed_code_pipe = parser.parse("[| | 1. ^2]")
	
	assert str(code_block) == str(parsed_code)
	assert str(code_block) == str(parsed_code_pipe)

def test_parses_code_args_block():
	parser = Parser()

	slots = [
		ArgumentSlotNode("arg"),
		DataSlotNode("a", "=", IntegerNode(2)),
		ParentSlotNode("b")
	]
	code_block = CodeNode([BlockNode(slots, CodeNode([IntegerNode(1), IntegerNode(2)]))])
	parsed_code = parser.parse("[|:arg. a = 2. b* | 1. 2]")
	
	assert str(code_block) == str(parsed_code)

def test_parses_block_with_more_than_one_argument():
	parser = Parser()

	slots = [
		ArgumentSlotNode("a"),
		ArgumentSlotNode("b"),
		ArgumentSlotNode("c")
	]
	code_block = CodeNode([BlockNode(slots, CodeNode([IntegerNode(1)]))])
	parsed_code = parser.parse("[| :a. :b. :c | 1]")
	
	assert str(code_block) == str(parsed_code)