from parsing.nodes.object_nodes.RegularObjectNode import *
from parsing.nodes.slot_nodes.DataSlotNode import *
from parsing.nodes.object_nodes.IntegerNode import *
from parsing.nodes.message_nodes.UnaryMessageNode import *
from interpreting.Interpreter import *
from parsing.utils.SelfSnippets import addPlusString

def test_basic_keyword_message_passing():
	# (| x: a Y: b = (| | a) |) x: 1 Y: ()
	interpreter = Interpreter()

	keyword_method_object = RegularObjectNode(code=CodeNode([UnaryMessageNode(None, 'a')]))
	keyword_slot = KeywordSlotNode(['x:', 'Y:'], keyword_method_object, ['a', 'b'])
	keyword_container = RegularObjectNode(slot_list_annotated=[keyword_slot])
	keyword_message = CodeNode([KeywordMessageNode(keyword_container, ["x:", "Y:"], [IntegerNode(1), RegularObjectNode()])])
	assert str(interpreter.interpret(keyword_message)) == str(SelfInteger(1))

def test_one_keyword_message_passing():
	# (| x: a = (| | a) |) x: 1
	interpreter = Interpreter()

	keyword_method_object = RegularObjectNode(code=CodeNode([UnaryMessageNode(None, "a")]))
	keyword_slot = KeywordSlotNode(["x:"], keyword_method_object, ["a"])
	keyword_container = RegularObjectNode(slot_list_annotated=[keyword_slot])
	keyword_message = CodeNode([KeywordMessageNode(keyword_container, ["x:"], [IntegerNode(1)])])
	assert str(interpreter.interpret(keyword_message)) == str(SelfInteger(1))

def test_multiple_keyword_message_passing():
	# (| x: a Y: b = (| | a + b) |) x: 1 Y: 2
	interpreter = Interpreter()
	parser = Parser()
	interpreter.interpret(parser.parse(addPlusString))

	keyword_method_object = RegularObjectNode(code=CodeNode([ BinaryMessageNode(UnaryMessageNode(None, "a"), "+", UnaryMessageNode(None, "b")) ]))
	keyword_slot = KeywordSlotNode(["x:", "Y:"], keyword_method_object, ["a", "b"])
	keyword_container = RegularObjectNode(slot_list_annotated=[keyword_slot])
	keyword_message = CodeNode([KeywordMessageNode(keyword_container, ["x:", "Y:"], [IntegerNode(1), IntegerNode(2)])])
	assert str(interpreter.interpret(keyword_message)) == str(SelfInteger(3))

def test_multiple_identical_keyword_message_passing():
	# (| x: a Y: b Y: c = (| | a + b + c) |) x: 1 Y: 2 Y: 3
	interpreter = Interpreter()
	parser = Parser()
	interpreter.interpret(parser.parse(addPlusString))

	keyword_method_object = RegularObjectNode(code=CodeNode([ BinaryMessageNode(BinaryMessageNode(UnaryMessageNode(None, "a"), "+", UnaryMessageNode(None, "b")), "+", UnaryMessageNode(None, "c")) ]))
	keyword_slot = KeywordSlotNode(["x:", "Y:", "Y:"], keyword_method_object, ["a", "b", "c"])
	keyword_container = RegularObjectNode(slot_list_annotated=[keyword_slot])
	keyword_message = CodeNode([KeywordMessageNode(keyword_container, ["x:", "Y:", "Y:"], [IntegerNode(1), IntegerNode(2), IntegerNode(3)])])
	assert str(interpreter.interpret(keyword_message)) == str(SelfInteger(6))