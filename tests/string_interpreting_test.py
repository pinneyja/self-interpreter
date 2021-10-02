import random
from parsing.nodes.StringNode import *
from interpreting.Interpreter import *


def test_interprets_basic_string():
	interpreter = Interpreter()
	parser_result = StringNode('test')
	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(SelfString('test'))

def test_interprets_escape_string():
	interpreter = Interpreter()
	parser_result = StringNode('\t\b\n\f\r\v\a\0\\\'\""?\xff')
	interpreted_result = interpreter.interpret(parser_result)

	assert str(interpreted_result) == str(SelfString('\t\b\n\f\r\v\a\0\\\'\"\"?\xff'))