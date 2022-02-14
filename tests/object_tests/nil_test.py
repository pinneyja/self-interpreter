from interpreting.Interpreter import Interpreter
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from parsing.Parser import Parser

def test_slot_initialized_to_nil():
	interpreter = Interpreter()
	parser = Parser()

	expected = SelfBoolean(True)

	actual = interpreter.interpret(parser.parse(
		"(|x|) x _Eq: nil"))

	assert str(actual) == str(expected)