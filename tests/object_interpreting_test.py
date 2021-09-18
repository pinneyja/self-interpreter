from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.IntegerNode import *
from interpreting.Environment import *
from src.Interpreter import *


def test_empty_object():
	interpreter = Interpreter()

	environment = Environment()
	parser_result = RegularObjectNode()

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == "SelfObject:{}"

def test_simple_object():
	interpreter = Interpreter()

	environment = Environment()
	parser_result = RegularObjectNode([DataSlotNode("x", "=", IntegerNode(4))])

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == "SelfObject:{SelfSlot:{name='x', value={SelfInteger: (value='4')}, isImmutable='True'},}"

def test_complicated_object():
	interpreter = Interpreter()

	environment = Environment()
	parser_result = RegularObjectNode([DataSlotNode("x", "=", IntegerNode(4)), DataSlotNode("y", "<-", RegularObjectNode([DataSlotNode("z", "=", IntegerNode(4))]))])

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == "SelfObject:{SelfSlot:{name='x', value={SelfInteger: (value='4')}, isImmutable='True'},SelfSlot:{name='y', value={SelfObject:{SelfSlot:{name='z', value={SelfInteger: (value='4')}, isImmutable='True'},}}, isImmutable='False'},}"