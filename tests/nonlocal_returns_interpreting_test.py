from interpreting.Interpreter import Interpreter
from interpreting.objects.SelfInteger import SelfInteger
from parsing.nodes.CodeNode import CodeNode
from parsing.nodes.BlockNode import BlockNode
from parsing.nodes.DataSlotNode import DataSlotNode
from parsing.nodes.ArgumentSlotNode import ArgumentSlotNode
from parsing.nodes.KeywordSlotNode import KeywordSlotNode
from parsing.nodes.IntegerNode import IntegerNode
from parsing.nodes.UnaryMessageNode import UnaryMessageNode
from parsing.nodes.BinaryMessageNode import BinaryMessageNode
from parsing.nodes.KeywordMessageNode import KeywordMessageNode
from parsing.nodes.RegularObjectNode import RegularObjectNode

def test_interprets_basic_return_block():
	# [^ 2] value
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(2)])
	inner_code.set_nonlocal_return(True)
	value_message = UnaryMessageNode(BlockNode(code=CodeNode([inner_code])), "value")
	code_node = CodeNode([value_message])

	expected_result = SelfInteger(2)
	interpreted_block = interpreter.interpret(code_node)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_nested_return_block():
	# [[^ 2] value. 9] value
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(2)])
	inner_code.set_nonlocal_return(True)
	value_message = UnaryMessageNode(BlockNode(code=CodeNode([inner_code])), "value")

	outer_value_message = UnaryMessageNode(BlockNode(code=CodeNode([value_message, IntegerNode(9)])), "value")
	code_node = CodeNode([outer_value_message])

	expected_result = SelfInteger(2)
	interpreted_block = interpreter.interpret(code_node)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_nested_return_block_in_object():
	# (| y = (| | [[^2] value. 9] value. 10) |) y
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(2)])
	inner_code.set_nonlocal_return(True)
	value_message = UnaryMessageNode(BlockNode(code=CodeNode([inner_code])), "value")

	outer_value_message = UnaryMessageNode(BlockNode(code=CodeNode([value_message, IntegerNode(9)])), "value")
	code_node = CodeNode([outer_value_message, IntegerNode(10)])

	inner_regular_object = RegularObjectNode(code=code_node)
	slot_list = [DataSlotNode("y", "=", inner_regular_object)]
	containing_object = RegularObjectNode(slot_list=slot_list)
	outer_unary_message = UnaryMessageNode(containing_object, "y")

	expected_result = SelfInteger(2)
	interpreted_block = interpreter.interpret(outer_unary_message)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_nested_return_block_in_object_in_code():
	# (| y = (| | [[^2] value. 9] value. 10) |) y. 11
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(2)])
	inner_code.set_nonlocal_return(True)
	value_message = UnaryMessageNode(BlockNode(code=CodeNode([inner_code])), "value")

	outer_value_message = UnaryMessageNode(BlockNode(code=CodeNode([value_message, IntegerNode(9)])), "value")
	code_node = CodeNode([outer_value_message, IntegerNode(10)])

	inner_regular_object = RegularObjectNode(code=code_node)
	slot_list = [DataSlotNode("y", "=", inner_regular_object)]
	containing_object = RegularObjectNode(slot_list=slot_list)
	outer_unary_message = UnaryMessageNode(containing_object, "y")
	code = CodeNode([outer_unary_message, IntegerNode(11)])

	expected_result = SelfInteger(11)
	interpreted_block = interpreter.interpret(code)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_passed_in_return_block():
	# (| doIt: b = (| | (b value: 1) + (b value: 2) ) |) doIt: [|:arg| ^arg]
	interpreter = Interpreter()

	part1 = KeywordMessageNode(UnaryMessageNode(None, "b"), ["value:"], [IntegerNode(1)])
	part2 = KeywordMessageNode(UnaryMessageNode(None, "b"), ["value:"], [IntegerNode(2)])
	inner_code_node = CodeNode([BinaryMessageNode(part1, "+", part2)])
	inner_regular_object = RegularObjectNode(code=inner_code_node)
	slot_list = [KeywordSlotNode(["doIt:"], inner_regular_object, ["b"])]
	containing_object = RegularObjectNode(slot_list=slot_list)
	in_block_code_node = CodeNode([UnaryMessageNode(None, "arg")])
	in_block_code_node.set_nonlocal_return(True)
	arg_block = BlockNode([ArgumentSlotNode("arg")], in_block_code_node)
	keyword_message = KeywordMessageNode(containing_object, ["doIt:"], [arg_block])
	code = CodeNode([keyword_message])

	expected_result = SelfInteger(1)
	interpreted_block = interpreter.interpret(code)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_return_in_unary_message():
	# ([^1] value) badMessage
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(1)])
	inner_code.set_nonlocal_return(True)
	inner_block = BlockNode(code=inner_code)
	containing_object = UnaryMessageNode(inner_block, "value")
	unary_message = UnaryMessageNode(containing_object, "badMessage")
	code = CodeNode([unary_message])

	expected_result = SelfInteger(1)
	interpreted_block = interpreter.interpret(code)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_return_in_binary_message_receiver():
	# ([^1] value) + ([^2] value)
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(1)])
	inner_code.set_nonlocal_return(True)
	inner_block = BlockNode(code=inner_code)
	containing_object = UnaryMessageNode(inner_block, "value")

	inner_code2 = CodeNode([IntegerNode(2)])
	inner_code2.set_nonlocal_return(True)
	inner_block2 = BlockNode(code=inner_code2)
	containing_object2 = UnaryMessageNode(inner_block2, "value")

	binary_message = BinaryMessageNode(containing_object, "+", containing_object2)
	code = CodeNode([binary_message])

	expected_result = SelfInteger(1)
	interpreted_block = interpreter.interpret(code)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_return_in_binary_message_argument():
	# ([1] value) + ([^2] value)
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(1)])
	inner_block = BlockNode(code=inner_code)
	containing_object = UnaryMessageNode(inner_block, "value")

	inner_code2 = CodeNode([IntegerNode(2)])
	inner_code2.set_nonlocal_return(True)
	inner_block2 = BlockNode(code=inner_code2)
	containing_object2 = UnaryMessageNode(inner_block2, "value")

	binary_message = BinaryMessageNode(containing_object, "+", containing_object2)
	code = CodeNode([binary_message])

	expected_result = SelfInteger(2)
	interpreted_block = interpreter.interpret(code)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_return_in_keyword_message_receiver():
	# ([^1] value) test: ([^2] value)
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(1)])
	inner_code.set_nonlocal_return(True)
	inner_block = BlockNode(code=inner_code)
	containing_object = UnaryMessageNode(inner_block, "value")

	inner_code2 = CodeNode([IntegerNode(2)])
	inner_code2.set_nonlocal_return(True)
	inner_block2 = BlockNode(code=inner_code2)
	containing_object2 = UnaryMessageNode(inner_block2, "value")

	keyword_message = KeywordMessageNode(containing_object, ["test:"], [containing_object2])
	code = CodeNode([keyword_message])

	expected_result = SelfInteger(1)
	interpreted_block = interpreter.interpret(code)

	assert str(expected_result) == str(interpreted_block)

def test_interprets_return_in_keyword_message_argument():
	# ([1] value) test: ([^2] value)
	interpreter = Interpreter()

	inner_code = CodeNode([IntegerNode(1)])
	inner_block = BlockNode(code=inner_code)
	containing_object = UnaryMessageNode(inner_block, "value")

	inner_code2 = CodeNode([IntegerNode(2)])
	inner_code2.set_nonlocal_return(True)
	inner_block2 = BlockNode(code=inner_code2)
	containing_object2 = UnaryMessageNode(inner_block2, "value")

	keyword_message = KeywordMessageNode(containing_object, ["test:"], [containing_object2])
	code = CodeNode([keyword_message])

	expected_result = SelfInteger(2)
	interpreted_block = interpreter.interpret(code)

	assert str(expected_result) == str(interpreted_block)