import random
from parsing.nodes.IntegerNode import *
from interpreting.Environment import *
from interpreting.Interpreter import *


def test_interprets_random_number():
	interpreter = Interpreter()

	for i in range (10):
		number = random.randint(-9999999, 9999999)

		parser_result = IntegerNode(number)
		interpreted_result = interpreter.interpret(parser_result)

		assert str(interpreted_result) == "SelfInteger: (value='{}')".format(number)
