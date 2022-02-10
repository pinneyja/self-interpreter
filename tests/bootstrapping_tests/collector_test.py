import pytest
from interpreting.Interpreter import Interpreter
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from parsing.Parser import Parser

@pytest.fixture(scope="module")
def interpreter():
	interpreter = Interpreter()
	interpreter.initializeBootstrap()
	return interpreter

def test_collector_asList(interpreter : Interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (| acc <- 0. itr <- 1|)"))
	interpreter.interpret(parser.parse("_AddSlots: (| test_list = (0 & 1 & 2 & 3 & 4) asList |)"))
	assert str(interpreter.interpret(parser.parse("test_list do: [| :val | acc: acc + (val * itr). itr: itr * 10]. acc"))) == str(SelfInteger(43210))

def test_collector_asVector(interpreter : Interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (| test_vector = (3 & 9 & 7) asVector |)"))
	assert str(interpreter.interpret(parser.parse("(test_vector _At: 0) + ((test_vector _At: 1)*10) + ((test_vector _At: 2)*100)"))) == str(SelfInteger(793))