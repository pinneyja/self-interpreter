from interpreting.Interpreter import Interpreter
from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
import pytest

@pytest.fixture(scope="module")
def interpreter():
	interpreter = Interpreter()
	interpreter.initializeBootstrap()
	return interpreter

def test_small_int_min_max(interpreter):
	parser = Parser()

	expected_max = SelfInteger(536870911)
	expected_min = SelfInteger(-536870912)

	actual_max = interpreter.interpret(parser.parse("maxSmallInt"))
	actual_min = interpreter.interpret(parser.parse("minSmallInt"))

	assert str(expected_max) == str(actual_max)
	assert str(expected_min) == str(actual_min)

def test_small_int_add(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-1222)
	expected_two = SelfInteger(-32441)
	expected_three = SelfInteger(234558)
	expected_four = SelfInteger(32400)

	actual_one = interpreter.interpret(parser.parse("-1234 + 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 + -7"))
	actual_three = interpreter.interpret(parser.parse("234234 + 324"))
	actual_four = interpreter.interpret(parser.parse("32434 + -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_subtract(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-1246)
	expected_two = SelfInteger(-32427)
	expected_three = SelfInteger(233910)
	expected_four = SelfInteger(32468)

	actual_one = interpreter.interpret(parser.parse("-1234 - 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 - -7"))
	actual_three = interpreter.interpret(parser.parse("234234 - 324"))
	actual_four = interpreter.interpret(parser.parse("32434 - -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_multiply(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-14808)
	expected_two = SelfInteger(227038)
	expected_three = SelfInteger(75891816)
	expected_four = SelfInteger(-1102756)

	actual_one = interpreter.interpret(parser.parse("-1234 * 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 * -7"))
	actual_three = interpreter.interpret(parser.parse("234234 * 324"))
	actual_four = interpreter.interpret(parser.parse("32434 * -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_divide(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-102)
	expected_two = SelfInteger(4633)
	expected_three = SelfInteger(722)
	expected_four = SelfInteger(-953)

	actual_one = interpreter.interpret(parser.parse("-1234 / 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 / -7"))
	actual_three = interpreter.interpret(parser.parse("234234 / 324"))
	actual_four = interpreter.interpret(parser.parse("32434 / -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_mod(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-10)
	expected_two = SelfInteger(-3)
	expected_three = SelfInteger(306)
	expected_four = SelfInteger(32)

	actual_one = interpreter.interpret(parser.parse("-1234 % 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 % -7"))
	actual_three = interpreter.interpret(parser.parse("234234 % 324"))
	actual_four = interpreter.interpret(parser.parse("32434 % -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_mod_plus(interpreter):
	parser = Parser()

	expected_one = SelfInteger(2)
	expected_two = SelfInteger(4)
	expected_three = SelfInteger(306)
	expected_four = SelfInteger(32)

	actual_one = interpreter.interpret(parser.parse("-1234 %+ 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 %+ -7"))
	actual_three = interpreter.interpret(parser.parse("234234 %+ 324"))
	actual_four = interpreter.interpret(parser.parse("32434 %+ -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_aritmetic_shift_left(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-5054464)
	expected_two = SelfInteger(-134217728)
	expected_three = SelfInteger(468468)
	expected_four = SelfInteger(0)

	actual_one = interpreter.interpret(parser.parse("-1234 <+ 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 <+ -6"))
	actual_three = interpreter.interpret(parser.parse("234234 <+ 1"))
	actual_four = interpreter.interpret(parser.parse("32434 <+ -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_aritmetic_shift_right(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-1)
	expected_two = SelfInteger(-1)
	expected_three = SelfInteger(117117)
	expected_four = SelfInteger(0)

	actual_one = interpreter.interpret(parser.parse("-1234 +> 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 +> -6"))
	actual_three = interpreter.interpret(parser.parse("234234 +> 1"))
	actual_four = interpreter.interpret(parser.parse("32434 +> -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_logical_shift_left(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-5054464)
	expected_two = SelfInteger(-134217728)
	expected_three = SelfInteger(468468)
	expected_four = SelfInteger(0)

	actual_one = interpreter.interpret(parser.parse("-1234 << 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 << -6"))
	actual_three = interpreter.interpret(parser.parse("234234 << 1"))
	actual_four = interpreter.interpret(parser.parse("32434 << -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_logical_shift_right(interpreter):
	parser = Parser()

	expected_one = SelfInteger(262143)
	expected_two = SelfInteger(15)
	expected_three = SelfInteger(117117)
	expected_four = SelfInteger(0)

	actual_one = interpreter.interpret(parser.parse("-1234 >> 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 >> -6"))
	actual_three = interpreter.interpret(parser.parse("234234 >> 1"))
	actual_four = interpreter.interpret(parser.parse("32434 >> -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_not_equal(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(True)
	expected_two = SelfBoolean(False)

	actual_one = interpreter.interpret(parser.parse("-1234 != 1234"))
	actual_two = interpreter.interpret(parser.parse("-32434 != -32434"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)

def test_small_int_less_than(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(True)
	expected_two = SelfBoolean(False)
	expected_three = SelfBoolean(False)

	actual_one = interpreter.interpret(parser.parse("-1234 < 1234"))
	actual_two = interpreter.interpret(parser.parse("-32434 < -32434"))
	actual_three = interpreter.interpret(parser.parse("32434 < -32434"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_small_int_less_than_or_equal(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(True)
	expected_two = SelfBoolean(True)
	expected_three = SelfBoolean(False)

	actual_one = interpreter.interpret(parser.parse("-1234 <= 1234"))
	actual_two = interpreter.interpret(parser.parse("-32434 <= -32434"))
	actual_three = interpreter.interpret(parser.parse("32434 <= -32434"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_small_int_greater_than(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(False)
	expected_two = SelfBoolean(False)
	expected_three = SelfBoolean(True)

	actual_one = interpreter.interpret(parser.parse("-1234 > 1234"))
	actual_two = interpreter.interpret(parser.parse("-32434 > -32434"))
	actual_three = interpreter.interpret(parser.parse("32434 > -32434"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_small_int_greater_than_or_equal(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(False)
	expected_two = SelfBoolean(True)
	expected_three = SelfBoolean(True)

	actual_one = interpreter.interpret(parser.parse("-1234 >= 1234"))
	actual_two = interpreter.interpret(parser.parse("-32434 >= -32434"))
	actual_three = interpreter.interpret(parser.parse("32434 >= -32434"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_small_int_equal(interpreter):
	parser = Parser()

	expected_one = SelfBoolean(False)
	expected_two = SelfBoolean(True)
	expected_three = SelfBoolean(False)

	actual_one = interpreter.interpret(parser.parse("-1234 = 1234"))
	actual_two = interpreter.interpret(parser.parse("-32434 = -32434"))
	actual_three = interpreter.interpret(parser.parse("32434 = -32434"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)

def test_small_int_and(interpreter):
	parser = Parser()

	expected_one = SelfInteger(12)
	expected_two = SelfInteger(-32440)
	expected_three = SelfInteger(64)
	expected_four = SelfInteger(32402)

	actual_one = interpreter.interpret(parser.parse("-1234 && 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 && -7"))
	actual_three = interpreter.interpret(parser.parse("234234 && 324"))
	actual_four = interpreter.interpret(parser.parse("32434 && -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_or(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-1234)
	expected_two = SelfInteger(-1)
	expected_three = SelfInteger(234494)
	expected_four = SelfInteger(-2)

	actual_one = interpreter.interpret(parser.parse("-1234 || 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 || -7"))
	actual_three = interpreter.interpret(parser.parse("234234 || 324"))
	actual_four = interpreter.interpret(parser.parse("32434 || -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_small_int_xor(interpreter):
	parser = Parser()

	expected_one = SelfInteger(-1246)
	expected_two = SelfInteger(32439)
	expected_three = SelfInteger(234430)
	expected_four = SelfInteger(-32404)

	actual_one = interpreter.interpret(parser.parse("-1234 ^^ 12"))
	actual_two = interpreter.interpret(parser.parse("-32434 ^^ -7"))
	actual_three = interpreter.interpret(parser.parse("234234 ^^ 324"))
	actual_four = interpreter.interpret(parser.parse("32434 ^^ -34"))

	assert str(expected_one) == str(actual_one)
	assert str(expected_two) == str(actual_two)
	assert str(expected_three) == str(actual_three)
	assert str(expected_four) == str(actual_four)

def test_integer_even_and_odd(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("2 even"))
	actual_two = interpreter.interpret(parser.parse("3 even"))
	actual_three = interpreter.interpret(parser.parse("2 odd"))
	actual_four = interpreter.interpret(parser.parse("3 odd"))

	assert str(SelfBoolean(True)) == str(actual_one)
	assert str(SelfBoolean(False)) == str(actual_two)
	assert str(SelfBoolean(False)) == str(actual_three)
	assert str(SelfBoolean(True)) == str(actual_four)

def test_integer_factorial(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("1 factorial"))
	actual_two = interpreter.interpret(parser.parse("10 factorial"))

	assert str(SelfInteger(1)) == str(actual_one)
	assert str(SelfInteger(3628800)) == str(actual_two)

def test_integer_factorial(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("1 fibonacci"))
	actual_two = interpreter.interpret(parser.parse("10 fibonacci"))

	assert str(SelfInteger(1)) == str(actual_one)
	assert str(SelfInteger(55)) == str(actual_two)

def test_number_absolute_value(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("1 absoluteValue"))
	actual_two = interpreter.interpret(parser.parse("-2 absoluteValue"))

	assert str(SelfInteger(1)) == str(actual_one)
	assert str(SelfInteger(2)) == str(actual_two)

def test_number_negate(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("1 negate"))
	actual_two = interpreter.interpret(parser.parse("-2 negate"))

	assert str(SelfInteger(-1)) == str(actual_one)
	assert str(SelfInteger(2)) == str(actual_two)

def test_number_square(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("7 square"))
	actual_two = interpreter.interpret(parser.parse("-8 square"))

	assert str(SelfInteger(49)) == str(actual_one)
	assert str(SelfInteger(64)) == str(actual_two)

def test_number_log(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("2 log: 1000"))

	assert str(SelfInteger(9)) == str(actual_one)

def test_number_max_and_min(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("7 max: 9"))
	actual_two = interpreter.interpret(parser.parse("-2 max: 0"))
	actual_three = interpreter.interpret(parser.parse("7 min: 9"))
	actual_four = interpreter.interpret(parser.parse("-2 min: 0"))

	assert str(SelfInteger(9)) == str(actual_one)
	assert str(SelfInteger(0)) == str(actual_two)
	assert str(SelfInteger(7)) == str(actual_three)
	assert str(SelfInteger(-2)) == str(actual_four)

def test_number_mean(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("7 mean: 9"))
	actual_two = interpreter.interpret(parser.parse("-2 mean: 2"))

	assert str(SelfInteger(8)) == str(actual_one)
	assert str(SelfInteger(0)) == str(actual_two)

def test_to_do(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (| x <- 0|)"))
	actual_one = interpreter.interpret(parser.parse("x: 0. 1 to: 10 ByPositive: 1 Do: [|:a. :b| x: x + a]. x"))
	actual_two = interpreter.interpret(parser.parse("x: 0. 1 to: 10 ByPositive: 2 Do: [|:a. :b| x: x + a]. x"))
	actual_three = interpreter.interpret(parser.parse("x: 0. -1 to: -10 ByNegative: -1 Do: [|:a. :b| x: x + a]. x"))
	actual_four = interpreter.interpret(parser.parse("x: 0. -1 to: -10 ByNegative: -2 Do: [|:a. :b| x: x + a]. x"))

	assert str(SelfInteger(55)) == str(actual_one)
	assert str(SelfInteger(25)) == str(actual_two)
	assert str(SelfInteger(-55)) == str(actual_three)
	assert str(SelfInteger(-25)) == str(actual_four)

def test_find_first(interpreter):
	parser = Parser()

	actual_one = interpreter.interpret(parser.parse("10 findFirst: [|:x. :i| (x * x) = 49] IfPresent: [|:x. :i| x] IfAbsent: -1"))
	actual_two = interpreter.interpret(parser.parse("10 findFirst: [|:x. :i| (x * x) = 50] IfPresent: [|:x. :i| x] IfAbsent: -1"))

	assert str(SelfInteger(7)) == str(actual_one)
	assert str(SelfInteger(-1)) == str(actual_two)