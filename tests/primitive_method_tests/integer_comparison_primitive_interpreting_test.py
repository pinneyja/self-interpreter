from interpreting.Interpreter import *
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger

def test_interprets_NE():
	interpreter = Interpreter()

	primitive_message_true = KeywordMessageNode(IntegerNode(1), ["_IntNE:"], [IntegerNode(2)])
	parser_result_true = CodeNode([primitive_message_true])
	interpreted_result_true = interpreter.interpret(parser_result_true)

	primitive_message_false = KeywordMessageNode(IntegerNode(1), ["_IntNE:"], [IntegerNode(1)])
	parser_result_false = CodeNode([primitive_message_false])
	interpreted_result_false = interpreter.interpret(parser_result_false)

	assert str(interpreted_result_true) == str(SelfBoolean(True))
	assert str(interpreted_result_false) == str(SelfBoolean(False))

def test_interprets_LT():
	interpreter = Interpreter()

	primitive_message_true = KeywordMessageNode(IntegerNode(1), ["_IntLT:"], [IntegerNode(2)])
	parser_result_true = CodeNode([primitive_message_true])
	interpreted_result_true = interpreter.interpret(parser_result_true)

	primitive_message_false = KeywordMessageNode(IntegerNode(1), ["_IntLT:"], [IntegerNode(1)])
	parser_result_false = CodeNode([primitive_message_false])
	interpreted_result_false = interpreter.interpret(parser_result_false)

	assert str(interpreted_result_true) == str(SelfBoolean(True))
	assert str(interpreted_result_false) == str(SelfBoolean(False))

def test_interprets_LE():
	interpreter = Interpreter()

	primitive_message_true = KeywordMessageNode(IntegerNode(1), ["_IntLE:"], [IntegerNode(1)])
	parser_result_true = CodeNode([primitive_message_true])
	interpreted_result_true = interpreter.interpret(parser_result_true)

	primitive_message_true_two = KeywordMessageNode(IntegerNode(1), ["_IntLE:"], [IntegerNode(2)])
	parser_result_true_two = CodeNode([primitive_message_true_two])
	interpreted_result_true_two = interpreter.interpret(parser_result_true_two)

	primitive_message_false = KeywordMessageNode(IntegerNode(1), ["_IntLE:"], [IntegerNode(0)])
	parser_result_false = CodeNode([primitive_message_false])
	interpreted_result_false = interpreter.interpret(parser_result_false)

	assert str(interpreted_result_true) == str(SelfBoolean(True))
	assert str(interpreted_result_true_two) == str(SelfBoolean(True))
	assert str(interpreted_result_false) == str(SelfBoolean(False))

def test_interprets_EQ():
	interpreter = Interpreter()

	primitive_message_true = KeywordMessageNode(IntegerNode(1), ["_IntEQ:"], [IntegerNode(1)])
	parser_result_true = CodeNode([primitive_message_true])
	interpreted_result_true = interpreter.interpret(parser_result_true)

	primitive_message_false = KeywordMessageNode(IntegerNode(1), ["_IntEQ:"], [IntegerNode(2)])
	parser_result_false = CodeNode([primitive_message_false])
	interpreted_result_false = interpreter.interpret(parser_result_false)

	assert str(interpreted_result_true) == str(SelfBoolean(True))
	assert str(interpreted_result_false) == str(SelfBoolean(False))

def test_interprets_GT():
	interpreter = Interpreter()

	primitive_message_true = KeywordMessageNode(IntegerNode(1), ["_IntGT:"], [IntegerNode(0)])
	parser_result_true = CodeNode([primitive_message_true])
	interpreted_result_true = interpreter.interpret(parser_result_true)

	primitive_message_false = KeywordMessageNode(IntegerNode(1), ["_IntGT:"], [IntegerNode(2)])
	parser_result_false = CodeNode([primitive_message_false])
	interpreted_result_false = interpreter.interpret(parser_result_false)

	assert str(interpreted_result_true) == str(SelfBoolean(True))
	assert str(interpreted_result_false) == str(SelfBoolean(False))

def test_interprets_GE():
	interpreter = Interpreter()

	primitive_message_true = KeywordMessageNode(IntegerNode(1), ["_IntGE:"], [IntegerNode(1)])
	parser_result_true = CodeNode([primitive_message_true])
	interpreted_result_true = interpreter.interpret(parser_result_true)

	primitive_message_true_two = KeywordMessageNode(IntegerNode(1), ["_IntGE:"], [IntegerNode(0)])
	parser_result_true_two = CodeNode([primitive_message_true_two])
	interpreted_result_true_two = interpreter.interpret(parser_result_true_two)

	primitive_message_false = KeywordMessageNode(IntegerNode(1), ["_IntGE:"], [IntegerNode(2)])
	parser_result_false = CodeNode([primitive_message_false])
	interpreted_result_false = interpreter.interpret(parser_result_false)

	assert str(interpreted_result_true) == str(SelfBoolean(True))
	assert str(interpreted_result_true_two) == str(SelfBoolean(True))
	assert str(interpreted_result_false) == str(SelfBoolean(False))

def test_prints_correct_error():
	interpreter = Interpreter()

	primitives = ["_IntNE:", "_IntLT:", "_IntLE:", "_IntEQ:", "_IntGT:", "_IntGE:"]

	for primitive in primitives:
		primitive_message = KeywordMessageNode(IntegerNode(1), [primitive], [RegularObjectNode()])
		parser_result = CodeNode([primitive_message])

		try:
			interpreted_result = interpreter.interpret(parser_result)
			assert False
		except SelfException as selfException:
			assert str(selfException) == str(SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive, SelfInteger(1), SelfObject())))