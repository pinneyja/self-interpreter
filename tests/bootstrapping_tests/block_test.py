from interpreting.Interpreter import Interpreter
from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger

def test_blocks_sum_numbers_zero_to_ten():
	interpreter = Interpreter()
	parser = Parser()

	expected = SelfInteger(55)
	
	interpreter.initializeBootstrap()
	actual = interpreter.interpret(parser.parse("lobby _AddSlots: (| i <- 0. sum <-0 |). [sum: sum + i. (i _IntEQ: 10) ifTrue: [^ sum] False: [i: i + 1]] loop"))

	assert str(actual) == str(expected)