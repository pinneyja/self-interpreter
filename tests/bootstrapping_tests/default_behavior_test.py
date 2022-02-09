from interpreting.Interpreter import Interpreter
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.SelfObject import SelfObject
from parsing.Parser import Parser
import pytest

@pytest.fixture(scope="module")
def interpreter():
	interpreter = Interpreter()
	interpreter.initializeBootstrap()
	return interpreter

def test_neq_comparison(interpreter):
	parser = Parser()

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("0 != 0"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("0 != 1"))
	assert str(actual) == str(expected)

	# This test case is blocked by float.self, should we leave commented to remember to add it in later?

	# expected = SelfBoolean(False)
	# actual = interpreter.interpret(parser.parse("1 != 1.0"))
	# assert str(actual) == str(expected)

	# Same case here, this test case is blocked by traits clonable

	# expected = SelfBoolean(True)
	# actual = interpreter.interpret(parser.parse("[] != []"))
	# assert str(actual) == str(expected)

def test_nil_comparison(interpreter):
	parser = Parser()

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("nil ifNil: true"))
	assert str(actual) == str(expected)

	expected = SelfInteger(0)
	actual = interpreter.interpret(parser.parse("0 ifNil: true"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("[ nil ifNotNil: true ] value _Eq: nil"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("0 ifNotNil: true"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("nil ifNil: true IfNotNil: false"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("0 ifNil: true IfNotNil: false"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("nil ifNotNil: false IfNil: true"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("nil isNil"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("0 isNil"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("nil isNotNil"))
	assert str(actual) == str(expected)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("0 isNotNil"))
	assert str(actual) == str(expected)

def test_value_with(interpreter):
	parser = Parser()

	expected = SelfObject()
	actual = interpreter.interpret(parser.parse("[] value"))
	assert str(actual) == str(expected)

	expected = SelfInteger(1)
	actual = interpreter.interpret(parser.parse("[|:a| a] value: 1"))
	assert str(actual) == str(expected)

	expected = SelfInteger(3)
	actual = interpreter.interpret(parser.parse("[|:a1. :a2| a1 + a2] value: 1 With: 2"))
	assert str(actual) == str(expected)

	expected = SelfInteger(6)
	actual = interpreter.interpret(parser.parse("[|:a1. :a2. :a3| a1 + a2 + a3] value: 1 With: 2 With: 3"))
	assert str(actual) == str(expected)

	expected = SelfInteger(21)
	actual = interpreter.interpret(parser.parse(
		"[|:a1. :a2. :a3. :a4. :a5. :a6| a1 + a2 + a3 + a4 + a5 + a6]" +
		"value: 1 With: 2 With: 3 With: 4 With: 5 With: 6 With: 7"))
	assert str(actual) == str(expected)

def test_value_with_too_many_withs(interpreter):
	parser = Parser()

	expected = SelfObject()
	actual = interpreter.interpret(parser.parse("[] value: 1"))
	assert str(actual) == str(expected)

	expected = SelfInteger(1)
	actual = interpreter.interpret(parser.parse("[|:a| a] value: 1 With: 2"))
	assert str(actual) == str(expected)