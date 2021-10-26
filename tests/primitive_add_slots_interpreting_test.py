from parsing.nodes.IntegerNode import *
from parsing.nodes.BinaryMessageNode import *
from parsing.nodes.KeywordMessageNode import *
from interpreting.objects.SelfInteger import *
from interpreting.objects.SelfSlot import *
from interpreting.Interpreter import *

def test_basic_add_slots():
	# () _AddSlots: (|x=2|)
	interpreter = Interpreter()

	parser_result = CodeNode([KeywordMessageNode(RegularObjectNode(), ["_AddSlots:"], [RegularObjectNode([DataSlotNode('x', '=', IntegerNode(2))])])])
	expected_result = SelfObject({
		'x' : SelfSlot('x', SelfInteger(2), is_immutable=True)
	})

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_overwrite_add_slots():
	# (|x=1|) _AddSlots: (|x=2|)
	interpreter = Interpreter()

	parser_result = CodeNode([KeywordMessageNode(
		RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))]), 
		["_AddSlots:"], 
		[RegularObjectNode([DataSlotNode('x', '=', IntegerNode(2))])])])
	expected_result = SelfObject({
		'x' : SelfSlot('x', SelfInteger(2), is_immutable=True)
	})

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)

def test_add_method_slots():
	# ((|y = 1|) _AddSlots: (|x = (| | y)|)) x
	interpreter = Interpreter()

	add_slots_container = RegularObjectNode([DataSlotNode('x', '=', RegularObjectNode(code=CodeNode([UnaryMessageNode(None, 'y')])))])
	add_slots_message = KeywordMessageNode(RegularObjectNode([DataSlotNode('y', '=', IntegerNode(1))]), ["_AddSlots:"], [add_slots_container])
	parser_result = CodeNode([UnaryMessageNode(add_slots_message, 'x')])
	expected_result = SelfInteger(1)

	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(expected_result)