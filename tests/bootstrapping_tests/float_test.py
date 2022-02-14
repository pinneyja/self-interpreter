from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean

def test_float_add(interpreter):
	parser = Parser()

	expected_one = SelfFloat(-1222.13)
	actual_one = interpreter.interpret(parser.parse("-1234.43 + 12.3"))

	assert str(expected_one) == str(actual_one)

def test_float_subtract(interpreter):
	parser = Parser()

	expected_one = SelfFloat(-1246.3)
	expected_two = SelfFloat(-1222.0)

	actual_one = interpreter.interpret(parser.parse("-1234.1 - 12.2"))
	actual_two = interpreter.interpret(parser.parse("-1234.1 - -12.1"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_mod(interpreter):
	parser = Parser()

	expected_one = SelfFloat(3.3 % 2.0)
	expected_two = SelfFloat(-3.3 % -1.0)

	actual_one = interpreter.interpret(parser.parse("3.3 % 2.0"))
	actual_two = interpreter.interpret(parser.parse("-3.3 % -1.0"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_multiply(interpreter):
	parser = Parser()

	expected_one = SelfFloat(3.3 * 2.7)
	expected_two = SelfFloat(-3.3 * 11.93)

	actual_one = interpreter.interpret(parser.parse("3.3 * 2.7"))
	actual_two = interpreter.interpret(parser.parse("-3.3 * 11.93"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_divide(interpreter):
	parser = Parser()

	expected_one = SelfFloat(3.3 / 2.7)
	expected_two = SelfFloat(-3.3 / 11.93)

	actual_one = interpreter.interpret(parser.parse("3.3 / 2.7"))
	actual_two = interpreter.interpret(parser.parse("-3.3 / 11.93"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_as_integer(interpreter):
	parser = Parser()

	expected_one = SelfInteger(2)
	expected_two = SelfInteger(-2)

	actual_one = interpreter.interpret(parser.parse("1.5 asInteger"))
	actual_two = interpreter.interpret(parser.parse("-2.5 asInteger"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_ceil(interpreter):
	parser = Parser()

	expected_one = SelfFloat(2.0)
	expected_two = SelfFloat(-2.0)

	actual_one = interpreter.interpret(parser.parse("1.5 ceil"))
	actual_two = interpreter.interpret(parser.parse("-2.1 ceil"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_floor(interpreter):
	parser = Parser()

	expected_one = SelfFloat(1.0)
	expected_two = SelfFloat(-3.0)

	actual_one = interpreter.interpret(parser.parse("1.5 floor"))
	actual_two = interpreter.interpret(parser.parse("-2.1 floor"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_round(interpreter):
	parser = Parser()

	expected_one = SelfFloat(2.0)
	expected_two = SelfFloat(-2.0)

	actual_one = interpreter.interpret(parser.parse("1.5 round"))
	actual_two = interpreter.interpret(parser.parse("-2.5 round"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_truncate(interpreter):
	parser = Parser()

	expected_one = SelfFloat(1.0)
	expected_two = SelfFloat(-2.0)

	actual_one = interpreter.interpret(parser.parse("1.5 truncate"))
	actual_two = interpreter.interpret(parser.parse("-2.5 truncate"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_not_equal(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(True)
	expected_two = SelfBoolean(False)

	actual_one = interpreter.interpret(parser.parse("-1234.1 != 1234.1"))
	actual_two = interpreter.interpret(parser.parse("-32434.23 != -32434.23"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_float_less_than(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(True)
	expected_two = SelfBoolean(False)
	expected_three = SelfBoolean(False)

	actual_one = interpreter.interpret(parser.parse("-1234.1 < 1234.1"))
	actual_two = interpreter.interpret(parser.parse("-32434.2 < -32434.2"))
	actual_three = interpreter.interpret(parser.parse("32434.3 < -32434.3"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_float_less_than_or_equal(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(True)
	expected_two = SelfBoolean(True)
	expected_three = SelfBoolean(False)

	actual_one = interpreter.interpret(parser.parse("-1234.1 <= 1234.1"))
	actual_two = interpreter.interpret(parser.parse("-32434.2 <= -32434.2"))
	actual_three = interpreter.interpret(parser.parse("32434.3 <= -32434.3"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_float_greater_than(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(False)
	expected_two = SelfBoolean(False)
	expected_three = SelfBoolean(True)

	actual_one = interpreter.interpret(parser.parse("-1234.1 > 1234.1"))
	actual_two = interpreter.interpret(parser.parse("-32434.2 > -32434.2"))
	actual_three = interpreter.interpret(parser.parse("32434.3 > -32434.3"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_float_greater_than_or_equal(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(False)
	expected_two = SelfBoolean(True)
	expected_three = SelfBoolean(True)

	actual_one = interpreter.interpret(parser.parse("-1234.1 >= 1234.1"))
	actual_two = interpreter.interpret(parser.parse("-32434.2 >= -32434.2"))
	actual_three = interpreter.interpret(parser.parse("32434.3 >= -32434.3"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_float_equal(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(False)
	expected_two = SelfBoolean(True)
	expected_three = SelfBoolean(False)

	actual_one = interpreter.interpret(parser.parse("-1234.1 = 1234.1"))
	actual_two = interpreter.interpret(parser.parse("-32434.2 = -32434.2"))
	actual_three = interpreter.interpret(parser.parse("32434.3 = -32434.3"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_number_absolute_value(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("1.0 absoluteValue"))
	actual_two = interpreter.interpret(parser.parse("-2.0 absoluteValue"))

	assert str(SelfFloat(1.0)) == str(actual_one)
	assert str(SelfFloat(2.0)) == str(actual_two)

def test_number_negate(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("1.1 negate"))
	actual_two = interpreter.interpret(parser.parse("-2.2 negate"))

	assert str(SelfFloat(-1.1)) == str(actual_one)
	assert str(SelfFloat(2.2)) == str(actual_two)

def test_int_as_float(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("1 asFloat"))
	actual_two = interpreter.interpret(parser.parse("-2 asFloat"))

	assert str(SelfFloat(1.0)) == str(actual_one)
	assert str(SelfFloat(-2.0)) == str(actual_two)