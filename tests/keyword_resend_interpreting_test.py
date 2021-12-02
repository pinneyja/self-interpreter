from interpreting.Interpreter import *

def test_undirected_resend():
	interpreter = Interpreter()

	# (| p* = (| x: a Y: b = (| | a + b) |). x = (| | resend.x: 1 Y: 2) |) x
	expected_output = SelfInteger(3)

	resend_msg = KeywordMessageNode(ResendNode('resend'), ["x:", "Y:"], [IntegerNode(1), IntegerNode(2)])
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([resend_msg])))
	binary_msg = BinaryMessageNode(UnaryMessageNode(None, 'a'), '+', UnaryMessageNode(None, 'b'))
	keyword_method_object = RegularObjectNode(None, CodeNode([binary_msg]))
	keyword_slot = KeywordSlotNode(["x:", "Y:"], keyword_method_object, ["a", "b"])
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([keyword_slot]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

def test_bad_undirected_resend():
	interpreter = Interpreter()

	# message not understood
	# (| p* = (| x: a = (| | a) |). x = (| | resend.bad: 1) |) x
	resend_msg = KeywordMessageNode(ResendNode('resend'), ["bad:"], [IntegerNode(1)])
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([resend_msg])))
	keyword_method_object = RegularObjectNode(None, CodeNode([UnaryMessageNode(None, 'a')]))
	keyword_slot = KeywordSlotNode(["x:"], keyword_method_object, ["a"])
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([keyword_slot]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])

	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.LOOKUP_ERROR_NO_SLOT.value.format("bad:")

	# ambiguous message
	# (| p1* = (| x: a = (| | 1) |). p2* = (| x: a = (| | 2) |). x = (| | resend.x: 1) |) x
	resend_msg = KeywordMessageNode(ResendNode('resend'), ["x:"], [IntegerNode(1)])
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([resend_msg])))

	keyword_method_object1 = RegularObjectNode(None, CodeNode([IntegerNode(1)]))
	keyword_slot1 = KeywordSlotNode(["x:"], keyword_method_object1, ["a"])
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([keyword_slot1]))
	keyword_method_object2 = RegularObjectNode(None, CodeNode([IntegerNode(2)]))
	keyword_slot2 = KeywordSlotNode(["x:"], keyword_method_object2, ["a"])
	p2_slot = ParentSlotNode('p2', '=', RegularObjectNode([keyword_slot2]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, x_slot]), 'x')])

	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.LOOKUP_ERROR_MULTIPLE_SLOTS.value.format("x:")
	
def test_directed_resend():
	interpreter = Interpreter()

	# (| p1* = (| x: a Y: b = (| | a + b) |). p2* = (| x: a Y: b = (| | a + b + 1) |). x = (| | p1.x: 1 Y: 2) |) x
	expected_output = SelfInteger(3)

	resend_msg = KeywordMessageNode(ResendNode('p1'), ["x:", "Y:"], [IntegerNode(1), IntegerNode(2)])
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([resend_msg])))

	binary_msg = BinaryMessageNode(UnaryMessageNode(None, 'a'), '+', UnaryMessageNode(None, 'b'))
	keyword_method_object1 = RegularObjectNode(None, CodeNode([binary_msg]))
	keyword_slot = KeywordSlotNode(["x:", "Y:"], keyword_method_object1, ["a", "b"])
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([keyword_slot]))

	binary_msg = BinaryMessageNode(BinaryMessageNode(UnaryMessageNode(None, 'a'), '+', UnaryMessageNode(None, 'b')), '+' , IntegerNode(1))
	keyword_method_object2 = RegularObjectNode(None, CodeNode([binary_msg]))
	keyword_slot = KeywordSlotNode(["x:", "Y:"], keyword_method_object2, ["a", "b"])
	p2_slot = ParentSlotNode('p2', '=', RegularObjectNode([keyword_slot]))

	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, x_slot]), 'x')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

	# (| p1* = (| x: a Y: b = (| | a + b) |). p2* = (| x: a Y: b = (| | a + b + 1) |). x = (| | p2.x: 1 Y: 2) |) x
	expected_output = SelfInteger(4)

	resend_msg = KeywordMessageNode(ResendNode('p2'), ["x:", "Y:"], [IntegerNode(1), IntegerNode(2)])
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([resend_msg])))

	binary_msg = BinaryMessageNode(UnaryMessageNode(None, 'a'), '+', UnaryMessageNode(None, 'b'))
	keyword_method_object1 = RegularObjectNode(None, CodeNode([binary_msg]))
	keyword_slot = KeywordSlotNode(["x:", "Y:"], keyword_method_object1, ["a", "b"])
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([keyword_slot]))

	binary_msg = BinaryMessageNode(BinaryMessageNode(UnaryMessageNode(None, 'a'), '+', UnaryMessageNode(None, 'b')), '+' , IntegerNode(1))
	keyword_method_object2 = RegularObjectNode(None, CodeNode([binary_msg]))
	keyword_slot = KeywordSlotNode(["x:", "Y:"], keyword_method_object2, ["a", "b"])
	p2_slot = ParentSlotNode('p2', '=', RegularObjectNode([keyword_slot]))

	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, x_slot]), 'x')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

def test_bad_directed_resend():
	interpreter = Interpreter()

	# (| p* = (| a = (| x: a Y: b = (| | a + b) |) |). x = (| | a.x: 1 Y: 2) |) x
	resend_msg = KeywordMessageNode(ResendNode('a'), ["x:", "Y:"], [IntegerNode(1), IntegerNode(2)])
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([resend_msg])))
	binary_msg = BinaryMessageNode(UnaryMessageNode(None, 'a'), '+', UnaryMessageNode(None, 'b'))
	keyword_method_object = RegularObjectNode(None, CodeNode([binary_msg]))
	keyword_slot = KeywordSlotNode(["x:", "Y:"], keyword_method_object, ["a", "b"])
	a_slot = DataSlotNode('a', '=', RegularObjectNode([keyword_slot]))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([a_slot]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])

	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.NO_DELEGATEE_SLOT.value.format("a")