from parsing.nodes.slot_nodes.DataSlotNode import *
from parsing.nodes.message_nodes.UnaryMessageNode import *
from parsing.nodes.slot_nodes.ParentSlotNode import *
from parsing.nodes.CodeNode import *
from parsing.nodes.object_nodes.RegularObjectNode import *
from parsing.nodes.object_nodes.IntegerNode import *
from interpreting.Interpreter import *

def test_undirected_resend():
	interpreter = Interpreter()

	# (| p* = (|a = 1|). x = (| | resend.a) |) x
	expected_output = SelfInteger(1)

	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("resend"), 'a')])))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([DataSlotNode('a', '=', IntegerNode(1))]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

def test_bad_undirected_resend():
	interpreter = Interpreter()

	# message not understood
	# (| p* = (|a = 1|). x = (| | resend.bad) |) x
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("resend"), 'bad')])))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([DataSlotNode('a', '=', IntegerNode(1))]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, x_slot]), 'x')])
	
	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.LOOKUP_ERROR_NO_SLOT.value.format("bad")

	# ambiguous message
	# (| p1* = (|a = 1|). p2* = (|a = 2|). x = (| | resend.a) |) x
	x_slot = DataSlotNode('x', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("resend"), 'a')])))
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([DataSlotNode('a', '=', IntegerNode(1))]))
	p2_slot = ParentSlotNode('p2', '=', RegularObjectNode([DataSlotNode('a', '=', IntegerNode(2))]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, x_slot]), 'x')])
	
	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.LOOKUP_ERROR_MULTIPLE_SLOTS.value.format("a")

def test_directed_resend():
	interpreter = Interpreter()

	# (| p1* = (|x = 1|). p2* = (|x = 2|). m = (| | p1.x) |) m
	expected_output = SelfInteger(1)

	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("p1"), 'x')])))
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))]))
	p2_slot = ParentSlotNode('p2', '=', RegularObjectNode([DataSlotNode('x', '=', IntegerNode(2))]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, m_slot]), 'm')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

	# (| p1* = (|x = 1|). p2* = (|x = 2|). m = (| | p2.x) |) m
	expected_output = SelfInteger(2)

	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("p2"), 'x')])))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, p2_slot, m_slot]), 'm')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

	# (| p1* = (|x = 1| 2). m = (| | p1.x) |) m
	expected_output = SelfInteger(1)
	p1_slot = ParentSlotNode('p1', '=', RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))], CodeNode([IntegerNode(2)])))
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("p1"), 'x')])))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p1_slot, m_slot]), 'm')])
	interpreted_node = interpreter.interpret(parsed_node)

	assert str(interpreted_node) == str(expected_output)

def test_bad_directed_resend():
	interpreter = Interpreter()

	# (| p* = (|x = 1|). m = (| | bad.x) |) m
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("bad"), 'x')])))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, m_slot]), 'm')])

	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.NO_DELEGATEE_SLOT.value.format("bad")

	# (| p* = (| a = (|x = 1|) |). m = (| | a.x) |) m
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(ResendNode("a"), 'x')])))
	a_slot = DataSlotNode('a', '=', RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))]))
	p_slot = ParentSlotNode('p', '=', RegularObjectNode([a_slot]))
	parsed_node = CodeNode([UnaryMessageNode(RegularObjectNode([p_slot, m_slot]), 'm')])

	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.NO_DELEGATEE_SLOT.value.format("a")

def test_correct_resend_reciever():
	parser = Parser()
	interpreter = Interpreter()
	
	result1 = interpreter.interpret(parser.parse("(| p* = (| m = (| | resend.m). p* = (| m = 1 |) |) |) m"))
	assert str(result1) == str(SelfInteger(1))

	result2 = interpreter.interpret(parser.parse("(| p* = (| m1 = (| | resend.m2). p* = (| m2 = 1 |). m2 = 2 |). m2 = 3 |) m1"))
	assert str(result2) == str(SelfInteger(1))
	
def test_resend_in_block(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("_AddSlots: (|x<-1|). _AddSlots: (|p*=(|x <- 2|)|). [resend.x] value"))
	actual_two = interpreter.interpret(parser.parse("_AddSlots: (| + = ( |:arg| 0 ) |) _AddSlots: (| p* = (| + = ( |:arg| arg ) |) |). [resend.+ 3] value"))
	actual_three = interpreter.interpret(parser.parse("_AddSlots: (| x: a = ( | | 0 ) |) _AddSlots: (| p* = (| x: a = ( | | a ) |) |). [resend.x: 3] value"))
	actual_four = interpreter.interpret(parser.parse("_AddSlots: (|x<-1|). _AddSlots: (|p*=(|x <- 2|)|). [[[resend.x] value] value] value"))

	expected_one = SelfInteger(2)
	expected_two = SelfInteger(3)
	expected_three = SelfInteger(3)
	expected_four = SelfInteger(2)

	assert str(actual_one) == str(expected_one)
	assert str(actual_two) == str(expected_two)
	assert str(actual_three) == str(expected_three)
	assert str(actual_four) == str(expected_four)
