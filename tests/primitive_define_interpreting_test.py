from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.Interpreter import *

def test_define_empty_obj():
	interpreter = Interpreter()
	# () _Define: (|x = 1|)
	receiver = RegularObjectNode()
	value = RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))])
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	expected_output = SelfObject({
		'x' : SelfSlot('x', SelfInteger(1), is_immutable=True)
	})
	assert str(expected_output) == str(interpreted_node)

	# (|x = 1|) _Define: ()
	receiver = RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))])
	value = RegularObjectNode()
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	expected_output = SelfObject()
	assert str(expected_output) == str(interpreted_node)

def test_define_override_data_slots():
	interpreter = Interpreter()
	# (|old = 1|) _Define: (|new = 2|)
	receiver = RegularObjectNode([DataSlotNode('old', '=', IntegerNode(1))])
	value = RegularObjectNode([DataSlotNode('new', '=', IntegerNode(2))])
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	expected_output = SelfObject({
		'new' : SelfSlot('new', SelfInteger(2), is_immutable=True)
	})
	assert str(expected_output) == str(interpreted_node)

	# (|a = 1. b = 2|) _Define: (|c = 3|)
	receiver = RegularObjectNode([DataSlotNode('a', '=', IntegerNode(1)), DataSlotNode('b', '=', IntegerNode(2))])
	value = RegularObjectNode([DataSlotNode('c', '=', IntegerNode(3))])
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	expected_output = SelfObject({
		'c' : SelfSlot('c', SelfInteger(3), is_immutable=True)
	})
	assert str(expected_output) == str(interpreted_node)

def test_define_multiple_slots():
	interpreter = Interpreter()
	# (|a = 1|) _Define: (|x = 2. y = 3|)
	receiver = RegularObjectNode([DataSlotNode('a', '=', IntegerNode(1))])
	value = RegularObjectNode([DataSlotNode('x', '=', IntegerNode(2)), DataSlotNode('y', '=', IntegerNode(3))])
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	expected_output = SelfObject({
		'x' : SelfSlot('x', SelfInteger(2), is_immutable=True),
		'y' : SelfSlot('y', SelfInteger(3), is_immutable=True)
	})
	assert str(expected_output) == str(interpreted_node)

def test_define_arg_slots():
	interpreter = Interpreter()
	# (| + arg = (| | arg) |) _Define: (|x = 1|)
	arg_obj_node = RegularObjectNode(code=CodeNode([UnaryMessageNode(None, "arg")]))
	receiver = RegularObjectNode([BinarySlotNode('+', arg_obj_node, 'arg')])
	value = RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))])
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	expected_output = SelfObject({
		'x' : SelfSlot('x', SelfInteger(1), is_immutable=True)
	})
	assert str(expected_output) == str(interpreted_node)

	# (|x = 1|) _Define: (| + arg = (| | arg) |)
	arg_code_node = CodeNode([UnaryMessageNode(None, "arg")])
	arg_obj_node = RegularObjectNode(code=arg_code_node)
	receiver = RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))])
	value = RegularObjectNode([BinarySlotNode('+', arg_obj_node, 'arg')])
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	arg_obj = SelfObject(None, {
		'arg' : SelfSlot('arg')
	}, code=arg_code_node)
	expected_output = SelfObject({
		'+' : SelfSlot('+', arg_obj, is_immutable=True)
	})
	assert str(expected_output) == str(interpreted_node)

def test_define_parent_slots():
	interpreter = Interpreter()
	# (| p* = () |) _Define: (|x = 1|)
	receiver = RegularObjectNode([ParentSlotNode('p', '=', RegularObjectNode())])
	value = RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))])
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	expected_output = SelfObject({
		'x' : SelfSlot('x', SelfInteger(1), is_immutable=True)
	})
	assert str(expected_output) == str(interpreted_node)

	# (|x = 1|) _Define: (| p* = () |)
	receiver = RegularObjectNode([DataSlotNode('x', '=', IntegerNode(1))])
	value = RegularObjectNode([ParentSlotNode('p', '=', RegularObjectNode())])
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])
	interpreted_node = interpreter.interpret(parsed_node)

	expected_output = SelfObject(parent_slots={
		'p' : SelfSlot('p', SelfObject(), is_immutable=True)
	})
	assert str(expected_output) == str(interpreted_node)

def test_define_bad_type_receiver():
	interpreter = Interpreter()
	# 5 _Define: ()
	receiver = IntegerNode(5)
	value = RegularObjectNode()
	define_msg = KeywordMessageNode(receiver, ['_Define:'], [value])
	parsed_node = CodeNode([define_msg])

	try:
		interpreted_node = interpreter.interpret(parsed_node)
		assert False
	except SelfException as e:
		assert str(e) == Messages.BAD_TYPE_ERROR.value.format('_Define:')

def test_retrieve_receiver_after_define():
	interpreter = Interpreter()
	# _AddSlots: (| x = (|a = 1|) |). x _Define: (|b = 2|). x b
	a_obj = RegularObjectNode([DataSlotNode('a', '=', IntegerNode(1))])
	x_obj = RegularObjectNode([DataSlotNode('x', '=', a_obj)])
	line1 = KeywordMessageNode(None, ['_AddSlots:'], [x_obj])

	receiver = UnaryMessageNode(None, 'x')
	value = RegularObjectNode([DataSlotNode('b', '=', IntegerNode(2))])
	line2 = KeywordMessageNode(receiver, ['_Define:'], [value])

	line3 = UnaryMessageNode(receiver, 'b')

	parsed_node = CodeNode([line1, line2, line3])
	interpreted_node = interpreter.interpret(parsed_node)
	expected_output = SelfInteger(2)
	assert str(expected_output) == str(interpreted_node)