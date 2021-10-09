from interpreting.Interpreter import *

def test_basic_argument_slot():
	# (|+ = (|:arg| arg)|)
	interpreter = Interpreter()

	inner_reg_object = RegularObjectNode([ ArgumentSlotNode("arg") ], UnaryMessageNode(None, "arg"))
	parser_result = RegularObjectNode([ BinarySlotNode("+", inner_reg_object) ])
	interpreted_result = interpreter.interpret(parser_result)

	method_object = SelfObject(OrderedDict(), OrderedDict([("arg", SelfSlot("arg"))]), code=UnaryMessageNode(None, "arg"))
	binary_slot = SelfSlot("+", method_object, True)
	expected_result = SelfObject(OrderedDict([("+", binary_slot)]), OrderedDict())

	assert str(interpreted_result) == str(expected_result)

def test_argument_slot_binary_message():
	# (|+ = (|:arg| arg)|) + 5
	interpreter = Interpreter()

	inner_reg_object = RegularObjectNode([ ArgumentSlotNode("arg") ], UnaryMessageNode(None, "arg"))
	reg_object = RegularObjectNode([ BinarySlotNode("+", inner_reg_object) ])
	parser_result = BinaryMessageNode(reg_object, "+", IntegerNode(5))
	interpreted_result = interpreter.interpret(parser_result)

	expected_result = SelfInteger(5)

	assert str(interpreted_result) == str(expected_result)

	# (|+ = (|:arg| arg x)|) + (|x = 5|)

	code_A = UnaryMessageNode(UnaryMessageNode(None, 'arg'), 'x')
	method_object_A = RegularObjectNode([ ArgumentSlotNode("arg") ], code_A)
	object_A = RegularObjectNode([ BinarySlotNode("+", method_object_A) ])
	slot_B = DataSlotNode('x', '=', IntegerNode(5))
	object_B = RegularObjectNode([ slot_B ])

	parser_result = BinaryMessageNode(object_A, "+", object_B)
	interpreted_result = interpreter.interpret(parser_result)

	expected_result = SelfInteger(5)

	assert str(interpreted_result) == str(expected_result)