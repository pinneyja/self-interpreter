from interpreting.Interpreter import *
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from Messages import *

def test_basic_parent_slot():
	# (| parent* = (|x=5|) |) x
	interpreter = Interpreter()

	inner_reg_object = RegularObjectNode([ DataSlotNode("x", "=", CodeNode([IntegerNode(5)])) ])
	reg_object = RegularObjectNode([ ParentSlotNode("parent", "=", inner_reg_object) ])
	parser_result = CodeNode([UnaryMessageNode(reg_object, "x")])
	interpreted_result = interpreter.interpret(parser_result)

	expected_result = SelfInteger(5)

	assert str(interpreted_result) == str(expected_result)

def test_nested_parent_slots():
	# (| parent* = (| parent2* = (|x=5|) |) |) x
	interpreter = Interpreter()

	inner_reg_object = RegularObjectNode([ DataSlotNode("x", "=", IntegerNode(5)) ])
	inner_reg_object2 = RegularObjectNode([ ParentSlotNode("parent2", "=", inner_reg_object) ])
	reg_object = RegularObjectNode([ ParentSlotNode("parent", "=", inner_reg_object2) ])
	parser_result = CodeNode([UnaryMessageNode(reg_object, "x")])
	interpreted_result = interpreter.interpret(parser_result)

	expected_result = SelfInteger(5)

	assert str(interpreted_result) == str(expected_result)

def test_nested_parent_slots_with_same_slot():
	# (| parent* = (| x = 4. parent2* = (|x=5|) |) |) x
	interpreter = Interpreter()

	inner_reg_object = RegularObjectNode([ DataSlotNode("x", "=", IntegerNode(5)) ])
	inner_reg_object2 = RegularObjectNode([ DataSlotNode("x", "=", IntegerNode(4)), ParentSlotNode("parent2", "=", inner_reg_object) ])
	reg_object = RegularObjectNode([ ParentSlotNode("parent", "=", inner_reg_object2) ])
	parser_result = CodeNode([UnaryMessageNode(reg_object, "x")])
	interpreted_result = interpreter.interpret(parser_result)

	expected_result = SelfInteger(4)

	assert str(interpreted_result) == str(expected_result)

def test_multiple_parent_slots():
	# (| parent* = (|x = 5|). parent2* = (|x = 4|) |) x
	interpreter = Interpreter()

	inner_reg_object = RegularObjectNode([ DataSlotNode("x", "=", IntegerNode(5)) ])
	inner_reg_object2 = RegularObjectNode([ DataSlotNode("x", "=", IntegerNode(4)) ])
	reg_object = RegularObjectNode([ ParentSlotNode("parent", "=", inner_reg_object2), ParentSlotNode("parent2", "=", inner_reg_object2) ])
	parser_result = CodeNode([UnaryMessageNode(reg_object, "x")])

	try:
		interpreted_result = interpreter.interpret(parser_result)
		assert False
	except SelfException as selfException:
		assert str(selfException) == Messages.LOOKUP_ERROR_MULTIPLE_SLOTS.value.format("x")

def test_parent_slot_loop():
	# (lobby _AddSlots: (|x* = (| y* = lobby |) |)) z
	interpreter = Interpreter()

	inner_object = RegularObjectNode([ ParentSlotNode("y", "=", UnaryMessageNode(None, "lobby")) ])
	outer_object = RegularObjectNode([ ParentSlotNode("x", "=", inner_object) ])
	keyword_message = KeywordMessageNode(UnaryMessageNode(None, "lobby"), ["_AddSlots:"], [outer_object])
	unary_message = UnaryMessageNode(keyword_message, "z")
	parser_result = CodeNode([unary_message])

	try:
		interpreted_result = interpreter.interpret(parser_result)
		assert False
	except SelfException as selfException:
		assert str(selfException) == Messages.LOOKUP_ERROR_NO_SLOT.value.format("z")