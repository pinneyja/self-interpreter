from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.Interpreter import Interpreter
from parsing.Parser import Parser
from parsing.utils.SelfSnippets import addPlusString

def test_basic_loop_with_restart():
	# lobby _AddSlots: (| x <- 0. y <-0 |). [x: x + 1. y: y + 1. (x _IntEQ: 3) ifTrue: [^ y] False: ['no']. _Restart] value
	interpreter = Interpreter()
	parser = Parser()
	interpreter.interpret(parser.parse(addPlusString))

	interpreted_result = interpreter.interpret(parser.parse("lobby _AddSlots: (| x <- 0. y <-0 |). [x: x + 1. y: y + 1. (x _IntEQ: 3) ifTrue: [^ y] False: ['no']. _Restart] value"))
	interpreted_result_two = interpreter.interpret(parser.parse("lobby x"))
	expected_result = SelfInteger(3)

	assert str(interpreted_result) == str(expected_result)
	assert str(interpreted_result_two) == str(expected_result)

def test_sum_numbers_zero_to_ten():
	# lobby _AddSlots: (| i <- 0. sum <-0 |). [sum: sum + i. (i _IntEQ: 10) ifTrue: [^ sum] False: ['no']. i: i + 1. _Restart] value
	interpreter = Interpreter()
	parser = Parser()
	interpreter.interpret(parser.parse(addPlusString))

	interpreted_result = interpreter.interpret(parser.parse("lobby _AddSlots: (| i <- 0. sum <-0 |). [sum: sum + i. (i _IntEQ: 10) ifTrue: [^ sum] False: ['no']. i: i + 1. _Restart] value"))
	interpreted_result_two = interpreter.interpret(parser.parse("lobby i"))
	expected_result = SelfInteger(55)
	expected_result_two = SelfInteger(10)

	assert str(interpreted_result) == str(expected_result)
	assert str(interpreted_result_two) == str(expected_result_two)