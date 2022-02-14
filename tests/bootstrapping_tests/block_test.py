from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger

def test_blocks_sum_numbers_zero_to_ten(interpreter):
	parser = Parser()

	expected = SelfInteger(55)
	actual = interpreter.interpret(parser.parse("lobby _AddSlots: (| i <- 0. sum <-0 |). [sum: sum + i. (i _IntEQ: 10) ifTrue: [^ sum] False: [i: i + 1]] loop"))

	assert str(actual) == str(expected)

def test_blocks_sum_numbers_zero_to_ten_with_while_false(interpreter):
	parser = Parser()

	expected = SelfInteger(55)
	actual = interpreter.interpret(parser.parse("_AddSlots: (| i <- 0. sum <- 0 |). [sum: sum + i. i: i + 1. i _IntEQ: 11] whileFalse: []. sum"))

	assert str(actual) == str(expected)

def test_loops_on_condition(interpreter):
	parser = Parser()

	expected = SelfInteger(10)

	actual = interpreter.interpret(parser.parse(
		"(| m = (| x <- 0 | [x _IntLT: 10] whileTrue: [x: x + 1]. x) |) m"))
	assert str(actual) == str(expected)

	actual = interpreter.interpret(parser.parse(
		"(| m = (| x <- 0 | [x: x + 1] untilTrue: [x _IntGT: 9]. x) |) m"))
	assert str(actual) == str(expected)

def test_block_exit(interpreter):
	parser = Parser()

	expected = SelfInteger(10)

	actual = interpreter.interpret(parser.parse(
		"(| m = (| x <- 0 | [|:exit| x: x + 10. exit value. x: x + 10] exit. x) |) m"))
	assert str(actual) == str(expected)

	actual = interpreter.interpret(parser.parse(
		"(| m = (| x <- 0 | [|:exit| (x _IntGE: 10) ifTrue: exit. x: x + 1] loopExit. x) |) m"))
	assert str(actual) == str(expected)

def test_block_exit_with_value(interpreter):
	parser = Parser()

	expected = SelfInteger(10)

	actual = interpreter.interpret(parser.parse(
		"(| m = (| x <- 0 | [|:exit| x: x + 10. exit value: x. x: x + 10] exitValue) |) m"))
	assert str(actual) == str(expected)

	actual = interpreter.interpret(parser.parse(
		"(| m =  (| x <- 0 | [|:exit| (x _IntGE: 10) ifTrue: [exit value: x]. x: x + 1] loopExitValue) |) m"))
	assert str(actual) == str(expected)