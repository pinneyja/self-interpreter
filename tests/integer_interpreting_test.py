from parsing.nodes.IntegerNode import *
from interpreting.Environment import *
from src.Interpreter import *


def test_interprets_random_number():
	interpreter = Interpreter()

	environment = Environment()
	rep_of_int = IntegerNode(5)
	rep_of_int = rep_of_int.interpret(environment)

	parser_result = IntegerNode(5)
	interpreted_result = interpreter.interpret(parser_result)

	assert str(rep_of_int) == str(interpreted_result)

def test_integers_unique_constraint():
	pass # TODO find a way to implement