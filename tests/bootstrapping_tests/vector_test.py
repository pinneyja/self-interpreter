from interpreting.Interpreter import Interpreter
from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfObjectVector import SelfObjectVector
import pytest

@pytest.fixture(scope="module")
def interpreter():
	interpreter = Interpreter()
	parser = Parser()
	interpreter.initializeBootstrap()
	return interpreter

def test_vector_at(interpreter):
	parser = Parser()

	expected = SelfInteger(2)

	interpreter.interpret(parser.parse("_AddSlots: (| v = vector _Clone: 4 Filler: 1 |)."))
	actual = interpreter.interpret(parser.parse("(v _At: 1) + (v at: 2 IfAbsent: [])"))

	assert str(expected) == str(actual)

def test_vector_at_put(interpreter):
	parser = Parser()

	expected = SelfInteger(16)

	interpreter.interpret(parser.parse("_AddSlots: (| v = vector _Clone: 4 Filler: 1 |)."))
	interpreter.interpret(parser.parse("v _At: 1 Put: 7. v at: 2 Put: 9 IfAbsent: []"))
	actual = interpreter.interpret(parser.parse("(v _At: 1) + (v at: 2 IfAbsent: [])"))

	assert str(expected) == str(actual)

def test_vector_clone(interpreter):
	parser = Parser()

	expected = SelfInteger(10)
	expected2 = SelfInteger(3)

	interpreter.interpret(parser.parse("_AddSlots: (| v = vector _Clone: 4 Filler: 1 |)."))
	interpreter.interpret(parser.parse("_AddSlots: (| v2 = v clone |)."))
	interpreter.interpret(parser.parse("v2 at: 2 Put: 9 IfAbsent: []"))
	actual = interpreter.interpret(parser.parse("(v at: 2 IfAbsent: []) + (v2 at: 2 IfAbsent: [])"))

	interpreter.interpret(parser.parse("_AddSlots: (| v2 = v copySize: 6 FillingWith: 2 |)."))
	actual2 = interpreter.interpret(parser.parse("(v2 at: 3 IfAbsent: []) + (v2 at: 5 IfAbsent: [])"))

	assert str(expected) == str(actual)
	assert str(expected2) == str(actual2)

def test_vector_size(interpreter):
	parser = Parser()

	expected = SelfInteger(6)

	interpreter.interpret(parser.parse("_AddSlots: (| v = vector _Clone: 4 Filler: 1 |)."))
	interpreter.interpret(parser.parse("_AddSlots: (| v2 = v cloneSize: 2 |)."))
	actual = interpreter.interpret(parser.parse("(v size) + (v2 size)"))

	assert str(expected) == str(actual)

def test_vector_range_copy(interpreter):
	parser = Parser()

	expected = SelfInteger(7)
	expected2 = SelfInteger(2)
	expected3 = SelfInteger(1)

	interpreter.interpret(parser.parse("_AddSlots: (| v = vector _Clone: 4 Filler: 1 |). v _At: 1 Put: 2."))
	interpreter.interpret(parser.parse("_AddSlots: (| v2 = vector _Clone: 3 Filler: 7 |)."))
	interpreter.interpret(parser.parse("v2 copyRangeDstPos: 1 SrcArray: v SrcPos: 1 Len: 2"))
	actual = interpreter.interpret(parser.parse("v2 _At: 0"))
	actual2 = interpreter.interpret(parser.parse("v2 _At: 1"))
	actual3 = interpreter.interpret(parser.parse("v2 _At: 2"))

	assert str(expected) == str(actual)
	assert str(expected2) == str(actual2)
	assert str(expected3) == str(actual3)

def test_vector_concatenate(interpreter):
	parser = Parser()

	expected = SelfInteger(7)
	expected2 = SelfInteger(2)
	expected3 = SelfInteger(1)

	interpreter.interpret(parser.parse("_AddSlots: (| v = vector _Clone: 4 Filler: 1 |). v _At: 1 Put: 2."))
	interpreter.interpret(parser.parse("_AddSlots: (| v2 = vector _Clone: 3 Filler: 7 |)."))
	interpreter.interpret(parser.parse("_AddSlots: (|v2 = v2 , v |)."))
	actual = interpreter.interpret(parser.parse("v2 _At: 0"))
	actual2 = interpreter.interpret(parser.parse("v2 _At: 4"))
	actual3 = interpreter.interpret(parser.parse("v2 _At: 6"))

	assert str(expected) == str(actual)
	assert str(expected2) == str(actual2)
	assert str(expected3) == str(actual3)