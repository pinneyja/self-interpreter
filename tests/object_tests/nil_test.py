from interpreting.Interpreter import Interpreter
from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from parsing.Parser import Parser
from parsing.Parser import UnaryMessageNode

def test_slot_initialized_to_nil():
	interpreter = Interpreter()
	parser = Parser()

	expected = SelfBoolean(True)

	interpreter.initializeBootstrap()
	actual = interpreter.interpret(parser.parse(
		"(|x|) x _Eq: nil"))

	assert str(actual) == str(expected)