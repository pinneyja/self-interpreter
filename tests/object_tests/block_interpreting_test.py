from typing import OrderedDict
from interpreting.Interpreter import Interpreter
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.SelfSlot import SelfSlot
from interpreting.objects.primitive_objects.SelfLobby import SelfLobby
from parsing.nodes.slot_nodes.ArgumentSlotNode import ArgumentSlotNode
from parsing.nodes.CodeNode import CodeNode
from parsing.nodes.object_nodes.BlockNode import BlockNode
from parsing.nodes.slot_nodes.DataSlotNode import DataSlotNode
from parsing.nodes.slot_nodes.KeywordSlotNode import KeywordSlotNode
from parsing.nodes.object_nodes.IntegerNode import IntegerNode
from parsing.nodes.slot_nodes.ParentSlotNode import ParentSlotNode
from parsing.nodes.message_nodes.UnaryMessageNode import UnaryMessageNode
from parsing.nodes.message_nodes.BinaryMessageNode import BinaryMessageNode
from parsing.nodes.message_nodes.KeywordMessageNode import KeywordMessageNode
from parsing.nodes.object_nodes.RegularObjectNode import RegularObjectNode

def test_interprets_empty_block():
	# []
	interpreter = Interpreter()

	empty_block_node = CodeNode([BlockNode()])
	empty_block = SelfObject({
		"value" : SelfSlot("value", SelfObject(parent_slots={
				"" : SelfSlot("", SelfLobby(), is_immutable=True)
			}), is_immutable=True)
	})
	interpreted_empty_block = interpreter.interpret(empty_block_node)

	assert str(empty_block) == str(interpreted_empty_block)

def test_interprets_code_block():
	# [1. 2]
	interpreter = Interpreter()

	code_block_node = CodeNode([BlockNode(code=CodeNode([IntegerNode(1), IntegerNode(2)]))])
	code_block = SelfObject({
		"value" : SelfSlot("value", SelfObject(parent_slots={
				"" : SelfSlot("", SelfLobby(), is_immutable=True)
			}, code=CodeNode([IntegerNode(1), IntegerNode(2)])), is_immutable=True)
	})
	interpreted_code_block = interpreter.interpret(code_block_node)

	assert str(code_block) == str(interpreted_code_block)

def test_interprets_code_args_block():
	# [|:arg. a = 2. b*| 1. 2]
	interpreter = Interpreter()

	slots = [
		ArgumentSlotNode("arg"),
		DataSlotNode("a", "=", IntegerNode(2)),
		ParentSlotNode("b")
	]
	code_block_node = CodeNode([BlockNode(slots, CodeNode([IntegerNode(1), IntegerNode(2)]))])

	code_block = SelfObject({
		"value:" : SelfSlot("value:", SelfObject(
			slots={
				"a" : SelfSlot("a", SelfInteger(2), True)
			},
			arg_slots={
				"arg" : SelfSlot("arg")
			},
			parent_slots={
				"b" : SelfSlot("b"),
				"" : SelfSlot("", SelfLobby(), is_immutable=True)
			}, 
			code=CodeNode([IntegerNode(1), IntegerNode(2)])), 
			is_immutable=True, 
			keyword_list=['value:'])
	})
	interpreted_code_block = interpreter.interpret(code_block_node)

	assert str(code_block) == str(interpreted_code_block)

def test_interprets_block_with_more_than_one_argument():
	# [|:a. :b. :c| ((a + b) + c)]
	# [|:a. :b. :c| ((a + b) + c)] value: 1 With: 2 With: 3
	interpreter = Interpreter()

	slots = [
		ArgumentSlotNode("a"),
		ArgumentSlotNode("b"),
		ArgumentSlotNode("c")
	]
	inner_code_node = CodeNode([BinaryMessageNode(BinaryMessageNode(UnaryMessageNode(None, "a"), "+", UnaryMessageNode(None, "b")), "+", UnaryMessageNode(None, "c"))])
	block_node = BlockNode(slots, inner_code_node)
	code_block_node = CodeNode([block_node])
	keyword_message_node = KeywordMessageNode(block_node, ["value:", "With:", "With:"], [IntegerNode(1), IntegerNode(2), IntegerNode(3)])

	code_block = SelfObject({
		"value:With:With:" : SelfSlot("value:With:With:", SelfObject(
			arg_slots={
				"a" : SelfSlot("a"),
				"b" : SelfSlot("b"),
				"c" : SelfSlot("c")
			},
			parent_slots={
				"" : SelfSlot("", SelfLobby(), is_immutable=True)
			}, 
			code=CodeNode([BinaryMessageNode(BinaryMessageNode(UnaryMessageNode(None, "a"), "+", UnaryMessageNode(None, "b")), "+", UnaryMessageNode(None, "c"))])), 
			is_immutable=True, 
			keyword_list=['value:', "With:", "With:"])
	})
	expected_keyword_message_result = SelfInteger(6)

	interpreted_code_block = interpreter.interpret(code_block_node)
	interpreted_keyword_message = interpreter.interpret(keyword_message_node)

	assert str(code_block) == str(interpreted_code_block)
	assert str(expected_keyword_message_result) == str(interpreted_keyword_message)

def test_interprets_block_in_context():
	# (|a = 1. x = (|b=2| [a + b] value) |) x
	interpreter = Interpreter()
	
	inner_code_block_node = CodeNode([UnaryMessageNode(BlockNode(code=CodeNode([BinaryMessageNode(UnaryMessageNode(None, "a"), "+", UnaryMessageNode(None, "b"))])), "value")])
	inner_slots = [DataSlotNode("b", "=", IntegerNode(2))]
	inner_object = RegularObjectNode(inner_slots, code=inner_code_block_node)
	slots = [
		DataSlotNode("a", "=", IntegerNode(1)),
		DataSlotNode("x", "=", inner_object),
	]
	code_block_node = CodeNode([UnaryMessageNode(RegularObjectNode(slots), "x")])

	expected = SelfInteger(3)

	interpreted_code_block = interpreter.interpret(code_block_node)

	assert str(expected) == str(interpreted_code_block)

def test_block_saves_context_from_creation():
	# (| x = (| a = 1| y: [a]). y: block = (|a = 2| block value) |) x
	interpreter = Interpreter()

	inner_code_node = CodeNode([KeywordMessageNode(None, ["y:"], [BlockNode(code=CodeNode([UnaryMessageNode(None, "a")]))])])
	inner_slots = [DataSlotNode("a", "=", IntegerNode(1))]
	inner_object = RegularObjectNode(inner_slots, code=inner_code_node)

	inner_code_node2 = CodeNode([UnaryMessageNode(UnaryMessageNode(None, "block"), "value")])
	inner_slots2 = [DataSlotNode("a", "=", IntegerNode(2))]
	inner_object2 = RegularObjectNode(inner_slots2, code=inner_code_node2)

	slots = [
		DataSlotNode("x", "=", inner_object),
		KeywordSlotNode(["y:"], inner_object2, ["block"])
	]
	code_node = CodeNode([UnaryMessageNode(RegularObjectNode(slots), "x")])

	expected = SelfInteger(1)

	interpreted = interpreter.interpret(code_node)

	assert str(expected) == str(interpreted)

def test_interprets_block_in_context_complicated():
	# (| doIt: block = (| | (block value: 1) + (block value: 2)) |) doIt: [|:arg| arg + arg]
	interpreter = Interpreter()
	
	part1 = KeywordMessageNode(UnaryMessageNode(None, "block"), ["value:"], [IntegerNode(1)])
	part2 = KeywordMessageNode(UnaryMessageNode(None, "block"), ["value:"], [IntegerNode(2)])
	inner_code_block_node = CodeNode([BinaryMessageNode(part1, "+", part2)])
	inner_object = RegularObjectNode(code=inner_code_block_node)
	slots = [KeywordSlotNode(["doIt:"], inner_object, ["block"]),]
	arg_block_node = BlockNode([ArgumentSlotNode("arg")], CodeNode([BinaryMessageNode(UnaryMessageNode(None, "arg"), "+", UnaryMessageNode(None, "arg"))]))
	code_block_node = CodeNode([KeywordMessageNode(RegularObjectNode(slots), ["doIt:"], [arg_block_node])])

	expected = SelfInteger(6)

	interpreted_code_block = interpreter.interpret(code_block_node)

	assert str(expected) == str(interpreted_code_block)