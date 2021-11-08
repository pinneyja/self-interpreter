from interpreting.Interpreter import *
from interpreting.objects.SelfBoolean import *
from parsing.nodes.RealNode import *

def test_eq_numbers():
	# 1 _Eq: 1
	interpreter = Interpreter()
	parser_result = CodeNode([KeywordMessageNode(IntegerNode(1), ["_Eq:"], [IntegerNode(1)])])
	expected_result = SelfBoolean(True)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

	# 1 _Eq: 10
	parser_result = CodeNode([KeywordMessageNode(IntegerNode(1), ["_Eq:"], [IntegerNode(10)])])
	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

	# 1.02e1 _Eq: 1.02e1
	parser_result = CodeNode([KeywordMessageNode(RealNode(10.2), ["_Eq:"], [RealNode(10.2)])])
	expected_result = SelfBoolean(True)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

	# 1.02e1 _Eq: 1.02e2
	parser_result = CodeNode([KeywordMessageNode(RealNode(10.2), ["_Eq:"], [RealNode(102.0)])])
	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

	# 1.02e1 _Eq: 1.01e1
	parser_result = CodeNode([KeywordMessageNode(RealNode(10.2), ["_Eq:"], [RealNode(10.1)])])
	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

def test_eq_different_types():
	# 10 _Eq: 1e1
	interpreter = Interpreter()
	parser_result = CodeNode([KeywordMessageNode(IntegerNode(10), ["_Eq:"], [RealNode(10.0)])])
	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

	# 1 _Eq: ()
	parser_result = CodeNode([KeywordMessageNode(IntegerNode(1), ["_Eq:"], [RegularObjectNode()])])
	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

	# (|x = 1|) _Eq: (|x = 2|) x
	receiver = RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))])
	argument = UnaryMessageNode(RegularObjectNode([DataSlotNode('x', '=', IntegerNode(2))]), 'x')
	parser_result = CodeNode([KeywordMessageNode(receiver, ["_Eq:"], [argument])])
	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

def test_eq_equal_not_identical():
	# () _Eq: ()
	interpreter = Interpreter()
	receiver = RegularObjectNode()
	argument = RegularObjectNode()
	parser_result = CodeNode([KeywordMessageNode(receiver, ["_Eq:"], [argument])])
	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

	# (|x = (). m = (| | x _Eq: ())|) m
	x_slot = DataSlotNode('x', '=', RegularObjectNode())
	keyword_msg = KeywordMessageNode(UnaryMessageNode(None, 'x'), ["_Eq:"], [RegularObjectNode()])
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([keyword_msg])))
	parser_result = CodeNode([UnaryMessageNode(RegularObjectNode([x_slot, m_slot]), 'm')])
	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

def test_eq_from_diff_msgs():
	# (|x = (). y = (| | x). m = (| | x _Eq: y)|) m
	interpreter = Interpreter()
	x_slot = DataSlotNode('x', '=', RegularObjectNode())
	y_slot = DataSlotNode('y', '=', RegularObjectNode(None, CodeNode([UnaryMessageNode(None, 'x')])))
	keyword_msg = KeywordMessageNode(UnaryMessageNode(None, 'x'), ["_Eq:"], [UnaryMessageNode(None, 'y')])
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([keyword_msg])))
	parser_result = CodeNode([UnaryMessageNode(RegularObjectNode([x_slot, y_slot, m_slot]), 'm')])
	expected_result = SelfBoolean(True)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)

def test_eq_same_object():
	# (|x = (). m = (| | x _Eq: x)|) m
	interpreter = Interpreter()
	x_slot = DataSlotNode('x', '=', RegularObjectNode())
	keyword_msg = KeywordMessageNode(UnaryMessageNode(None, 'x'), ["_Eq:"], [UnaryMessageNode(None, 'x')])
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, CodeNode([keyword_msg])))
	parser_result = CodeNode([UnaryMessageNode(RegularObjectNode([x_slot, m_slot]), 'm')])
	expected_result = SelfBoolean(True)
	interpreted_result = interpreter.interpret(parser_result)
	assert str(interpreted_result) == str(expected_result)