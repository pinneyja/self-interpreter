from interpreting.Interpreter import Interpreter
from parsing.nodes.IntegerNode import *
from parsing.nodes.CodeNode import *

def test_basic_code():
	interpreter = Interpreter() 
	code = CodeNode([IntegerNode(1), IntegerNode(2), IntegerNode(3)])

	assert str(interpreter.interpret(code)) == str(SelfInteger(3))