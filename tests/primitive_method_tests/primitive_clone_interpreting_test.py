from parsing.Parser import Parser
from interpreting.Interpreter import *
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from parsing.utils.SelfSnippets import addPlusString

def test_clone_simple():
	parser = Parser()
	interpreter = Interpreter()

	interpreted_result = interpreter.interpret(parser.parse("_AddSlots: (|obj1 = (|x<-1. z<-2|)|). _AddSlots: (|obj2 = obj1 _Clone|). obj2 x"))
	assert str(interpreted_result) == str(SelfInteger(1))

def test_clone_with_mutation():
	parser = Parser()
	interpreter = Interpreter()
	interpreter.interpret(parser.parse(addPlusString))

	interpreted_result = interpreter.interpret(parser.parse("_AddSlots: (|obj1 = (|x<-1. z<-2|)|). _AddSlots: (|obj2 = obj1 _Clone|). obj1 x: 5. obj1 x + obj2 x"))
	assert str(interpreted_result) == str(SelfInteger(6))

def test_clone_shallow_copy():
	parser = Parser()
	interpreter = Interpreter()

	interpreted_result = interpreter.interpret(parser.parse("_AddSlots: (|obj1 = (|inner = (|x<-1|)|)|). _AddSlots: (|obj2 = obj1 _Clone|). obj2 inner x: 3. obj1 inner x"))
	assert str(interpreted_result) == str(SelfInteger(3))

def test_clone_works_with_special_primitives():
	parser = Parser()
	interpreter = Interpreter()

	interpreted_result = interpreter.interpret(parser.parse("_AddSlots: (|x<-'test'|). x _Eq: (x _Clone)"))
	assert str(interpreted_result) == str(SelfBoolean(True))

	interpreted_result = interpreter.interpret(parser.parse("_AddSlots: (|x<-2|). x _Eq: (x _Clone)"))
	assert str(interpreted_result) == str(SelfBoolean(True))

	interpreted_result = interpreter.interpret(parser.parse("_AddSlots: (|x<-2.34|). x _Eq: (x _Clone)"))
	assert str(interpreted_result) == str(SelfBoolean(True))