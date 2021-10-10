from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.IntegerNode import *
from parsing.nodes.UnaryMessageNode import *
from interpreting.Interpreter import *

def test_basic_binary_message_passing():
	# (| + = (|:arg| 5)|) + 1
	interpreter = Interpreter()

	reg_object = RegularObjectNode([ DataSlotNode("+", "=", RegularObjectNode([ArgumentSlotNode("arg")], IntegerNode(5))) ])
	parser_result = BinaryMessageNode(reg_object, "+", IntegerNode(1))
	interpreted_result = interpreter.interpret(parser_result)

	expected_result = SelfInteger(5)

	assert str(interpreted_result) == str(expected_result)