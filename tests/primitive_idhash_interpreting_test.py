from interpreting.Interpreter import *
from interpreting.objects.SelfBoolean import *
import random

def test_idhash_numbers():
	interpreter = Interpreter()
	for i in range(10):
		number = random.randint(-9999999, 9999999)

		expected_node = SelfInteger(number)
		if (number == -1):
			expected_node = SelfInteger(-2)

		parser_result = CodeNode([UnaryMessageNode(IntegerNode(number), "_IdentityHash")])
		interpreted_result = interpreter.interpret(parser_result)

		assert str(interpreted_result) == str(expected_node)

	for i in range(10):
		number = random.uniform(-9999999, 9999999)

		parser_result = CodeNode([UnaryMessageNode(RealNode(number), "_IdentityHash")])
		interpreted_result_1 = interpreter.interpret(parser_result)
		interpreted_result_2 = interpreter.interpret(parser_result)

		assert str(interpreted_result_1) == str(interpreted_result_2)

def test_eq_numval_have_eq_hashes():
	interpreter = Interpreter()
	expected_result = SelfBoolean(True)

	# 1 _IdentityHash _Eq: 1.0 _IdentityHash
	id_msg_int = UnaryMessageNode(IntegerNode(1), '_IdentityHash')
	id_msg_float = UnaryMessageNode(RealNode(1.0), '_IdentityHash')
	eq_msg = KeywordMessageNode(id_msg_int, ["_Eq:"], [id_msg_float])
	parsed_node = CodeNode([eq_msg])
	interpreted_result = interpreter.interpret(parsed_node)

	assert str(interpreted_result) == str(expected_result)

def test_eq_objs_have_eq_hashes():
	interpreter = Interpreter()
	expected_result = SelfBoolean(True)

	# (|x = (). m = (| | x _IdentityHash _Eq: x _IdentityHash)|) m
	id_msg = UnaryMessageNode(UnaryMessageNode(None, 'x'), '_IdentityHash')
	eq_msg = KeywordMessageNode(id_msg, ["_Eq:"], [id_msg])
	x_slot = DataSlotNode('x', '=', RegularObjectNode())
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, eq_msg))
	obj = RegularObjectNode([x_slot, m_slot])
	parsed_node = CodeNode([UnaryMessageNode(obj, 'm')])
	interpreted_result = interpreter.interpret(parsed_node)

	assert str(interpreted_result) == str(expected_result)

	# (|x = (). y = (| | x). m = (| | x _IdentityHash _Eq: y _IdentityHash)|) m
	id_msg_x = UnaryMessageNode(UnaryMessageNode(None, 'x'), '_IdentityHash')
	id_msg_y = UnaryMessageNode(UnaryMessageNode(None, 'y'), '_IdentityHash')
	eq_msg = KeywordMessageNode(id_msg_x, ["_Eq:"], [id_msg_y])
	x_slot = DataSlotNode('x', '=', RegularObjectNode())
	y_slot = DataSlotNode('y', '=', RegularObjectNode(None, UnaryMessageNode(None, 'x')))
	m_slot = DataSlotNode('m', '=', RegularObjectNode(None, eq_msg))
	obj = RegularObjectNode([x_slot, y_slot, m_slot])
	parsed_node = CodeNode([UnaryMessageNode(obj, 'm')])
	interpreted_result = interpreter.interpret(parsed_node)

	assert str(interpreted_result) == str(expected_result)

	# 5 _IdentityHash _Eq: 5 _IdentityHash
	id_msg = UnaryMessageNode(IntegerNode(5), '_IdentityHash')
	parsed_node = KeywordMessageNode(id_msg, ["_Eq:"], [id_msg])
	interpreted_result = interpreter.interpret(parsed_node)

	assert str(interpreted_result) == str(expected_result)

def test_objs_in_lobby_diff_hashes():
	interpreter = Interpreter()
	
	# [_AddSlots: (|x = (). y = ()|). x _IdentityHash _Eq: y _IdentityHash] value
	x_slot = DataSlotNode("x", "=", RegularObjectNode())
	y_slot = DataSlotNode("y", "=", RegularObjectNode())
	obj_with_slots = RegularObjectNode([x_slot, y_slot])
	line1 = KeywordMessageNode(None, ["_AddSlots:"], [obj_with_slots])
	x_idmsg = UnaryMessageNode(UnaryMessageNode(None, "x"), "_IdentityHash")
	y_idmsg = UnaryMessageNode(UnaryMessageNode(None, "y"), "_IdentityHash")
	line2 = KeywordMessageNode(x_idmsg, ["_Eq:"], [y_idmsg])
	block_node = BlockNode(code=CodeNode([line1, line2]))
	parsed_node = CodeNode([UnaryMessageNode(block_node, "value")])

	expected_result = SelfBoolean(False)
	interpreted_result = interpreter.interpret(parsed_node)

	assert str(interpreted_result) == str(expected_result)