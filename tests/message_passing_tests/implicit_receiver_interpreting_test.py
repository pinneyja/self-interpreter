from interpreting.Interpreter import *
from parsing.nodes.object_nodes.RegularObjectNode import *
from parsing.nodes.message_nodes.UnaryMessageNode import *
from parsing.nodes.object_nodes.IntegerNode import *
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from Messages import *

def test_basic_valid_implicit_message_passing():
	# lobby
	interpreter = Interpreter()
	
	unary_message = CodeNode([UnaryMessageNode(None, "lobby")])
	interpreted_result = interpreter.interpret(unary_message)
	
	assert str(interpreted_result) == str(SelfLobby())

def test_implicit_message_passing_in_method_slot():
	# (| object1 = (| int1 = 1 | int1)|) object1
	interpreter = Interpreter()

	code = CodeNode([UnaryMessageNode(None, "int1")])
	slot_list = [ DataSlotNode("int1", "=", IntegerNode(1)) ]
	reg_object = RegularObjectNode(slot_list, code)
	slot_list1 = [ DataSlotNode("object1", "=", reg_object)]
	reg_object1 = RegularObjectNode(slot_list1)
	unary_message = CodeNode([UnaryMessageNode(reg_object1, "object1")])

	interpreted_result = interpreter.interpret(unary_message)

	assert str(interpreted_result) == str(SelfInteger(1))

def test_invalid_implicit_message_passing():
	# (| object1 = (| int1 = 1 | int2)|) object1
	interpreter = Interpreter()

	code = CodeNode([UnaryMessageNode(None, "int2")])
	slot_list = [ DataSlotNode("int1", "=", IntegerNode(1)) ]
	reg_object = RegularObjectNode(slot_list, code)
	slot_list1 = [ DataSlotNode("object1", "=", reg_object)]
	reg_object1 = RegularObjectNode(slot_list1)
	unary_message = CodeNode([UnaryMessageNode(reg_object1, "object1")])

	try:
		interpreted_result = interpreter.interpret(unary_message)
		assert False
	except SelfException as selfException:
		assert str(selfException) == Messages.LOOKUP_ERROR_NO_SLOT.value.format("int2")

def test_implicit_binary_message_passing_in_method_slot():
	# (| object1 = (| + arg = (| | 1) | + 5)|) object1
	interpreter = Interpreter()

	code = CodeNode([BinaryMessageNode(None, "+", IntegerNode(5))])
	slot_list = [ BinarySlotNode("+", RegularObjectNode(code=IntegerNode(1)), "arg") ]
	reg_object = RegularObjectNode(slot_list, code)
	slot_list1 = [ DataSlotNode("object1", "=", reg_object)]
	reg_object1 = RegularObjectNode(slot_list1)
	unary_message = CodeNode([UnaryMessageNode(reg_object1, "object1")])

	interpreted_result = interpreter.interpret(unary_message)

	assert str(interpreted_result) == str(SelfInteger(1))

def test_self_is_set_correctly():
	interpreter = Interpreter()
	parser = Parser()
	parsed_result = parser.parse("(| p: a = (| | _Eq: a). x = (| | p: self)|) x")

	assert str(interpreter.interpret(parsed_result)) == str(SelfBoolean(True))


def test_can_add_slots_in_method():
	interpreter = Interpreter()
	parser = Parser()
	result = interpreter.interpret(parser.parse("_AddSlots: (| m = (| | _AddSlots: (| x <- 1 |) ) |). m. x"))

	assert str(result) == str(SelfInteger(1))