from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.IntegerNode import *
from parsing.nodes.UnaryMessageNode import *
from interpreting.Interpreter import *

def test_basic_keyword_message_passing():
	# (| x: a Y: b = (| | 100) |) x: 1 Y: ()
	interpreter = Interpreter()

	keyword_method_object = RegularObjectNode(code=CodeNode([UnaryMessageNode(None, 'a')]))
	keyword_slot = KeywordSlotNode(['x:', 'Y:'], keyword_method_object, ['a', 'b'])
	keyword_container = RegularObjectNode(slot_list=[keyword_slot])
	keyword_message = CodeNode([KeywordMessageNode(keyword_container, ["x:", "Y:"], [IntegerNode(1), RegularObjectNode()])])
	assert str(interpreter.interpret(keyword_message)) == str(SelfInteger(1))
