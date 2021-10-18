from interpreting.Interpreter import Interpreter
from interpreting.objects.SelfException import *
from parsing.nodes.UnaryMessageNode import *
from parsing.nodes.KeywordMessageNode import *
from parsing.nodes.IntegerNode import *
from parsing.nodes.CodeNode import *
from Messages import *

def test_basic_code():
	# 1. 2. 3
	interpreter = Interpreter() 
	code = CodeNode([IntegerNode(1), IntegerNode(2), IntegerNode(3)])

	assert str(interpreter.interpret(code)) == str(SelfInteger(3))

def test_code_error():
	# 1. 1 x. 1 _Nonexistant: 3
	interpreter = Interpreter()
	code = CodeNode([IntegerNode(1), UnaryMessageNode(IntegerNode(1), "x"), KeywordMessageNode(IntegerNode(1), ["_Nonexistant:"], [IntegerNode(3)])])

	try:
		interpreter.interpret(code)
		assert False
	except SelfException as exception:
		assert str(exception) == Messages.LOOKUP_ERROR_NO_SLOT.value