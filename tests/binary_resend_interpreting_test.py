from interpreting.Interpreter import *

def test_undirected_resend():
	interpreter = Interpreter()

	# (| p* = (| + arg = (| | arg) |). x = (| | resend.+ 5) |) x
	expected_output = SelfInteger(5)
	
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([BinaryMessageNode(ResendNode("resend"), '+', IntegerNode(5))])))
	binary_slot = BinarySlotNode('+', RegularObjectNode(None, CodeNode([UnaryMessageNode(None, 'arg')])), 'arg')
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([binary_slot]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

def test_bad_undirected_resend():
	interpreter = Interpreter()

	# message not understood
	# (| p* = (|bad = 1|). x = (| | resend.+ 5) |) x
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([BinaryMessageNode(ResendNode("resend"), '+', IntegerNode(5))])))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([DataSlotNode('bad', '=', IntegerNode(1))]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])
	
	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.LOOKUP_ERROR_NO_SLOT.value.format("+")

	# ambiguous message
	# (| p1* = (| + arg = (| | 1) |). p2* = (| + arg = (| | 2) |). x = (| | resend.+ 5) |) x
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([BinaryMessageNode(ResendNode("resend"), '+', IntegerNode(5))])))

	binary_slot1 = BinarySlotNode('+', RegularObjectNode(None, CodeNode([IntegerNode(1)])), 'arg')
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([binary_slot1]))
	binary_slot2 = BinarySlotNode('+', RegularObjectNode(None, CodeNode([IntegerNode(2)])), 'arg')
	p2_slot = ParentSlotNode('p2', '=', RegularObjectNode([binary_slot2]))

	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, x_slot]), 'x')])
	
	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.LOOKUP_ERROR_MULTIPLE_SLOTS.value.format("+")

def test_directed_resend():
	interpreter = Interpreter()

	# (| p1* = (| + arg = (| | arg) |). p2* = (| + arg = (| | arg + 1) |). x = (| | p1.+ 5) |) x
	expected_output = SelfInteger(5)
	
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([BinaryMessageNode(ResendNode("p1"), '+', IntegerNode(5))])))
	binary_slot1 = BinarySlotNode('+', RegularObjectNode(None, CodeNode([UnaryMessageNode(None, 'arg')])), 'arg')
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([binary_slot1]))
	binary_slot2 = BinarySlotNode('+', RegularObjectNode(None, CodeNode([BinaryMessageNode(UnaryMessageNode(None, 'arg'), '+', IntegerNode(1))])), 'arg')
	p2_slot = ParentSlotNode('p2', '=', RegularObjectNode([binary_slot2]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, x_slot]), 'x')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

	# (| p1* = (| + arg = (| | arg) |). p2* = (| + arg = (| | arg + 1) |). x = (| | p2.+ 5) |) x
	expected_output = SelfInteger(6)
	
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([BinaryMessageNode(ResendNode("p2"), '+', IntegerNode(5))])))
	binary_slot1 = BinarySlotNode('+', RegularObjectNode(None, CodeNode([UnaryMessageNode(None, 'arg')])), 'arg')
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([binary_slot1]))
	binary_slot2 = BinarySlotNode('+', RegularObjectNode(None, CodeNode([BinaryMessageNode(UnaryMessageNode(None, 'arg'), '+', IntegerNode(1))])), 'arg')
	p2_slot = ParentSlotNode('p2', '=', RegularObjectNode([binary_slot2]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, x_slot]), 'x')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

def test_bad_directed_resend():
	interpreter = Interpreter()

	# (| p* = (| a = (| + arg = (| | arg) |) |). m = (| | a.+ 5) |) m
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([BinaryMessageNode(ResendNode("a"), '+', IntegerNode(5))])))
	binary_slot = BinarySlotNode('+', RegularObjectNode(None, CodeNode([UnaryMessageNode(None, 'arg')])), 'arg')
	a_slot = DataSlotNode('a', '=', RegularObjectNode([binary_slot]))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([a_slot]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, m_slot]), 'm')])

	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.NO_DELEGATEE_SLOT.value.format("a")
	