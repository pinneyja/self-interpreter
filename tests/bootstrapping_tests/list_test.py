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

def test_list_copy_size(interpreter : Interpreter):
	parser = Parser()

	assert str(interpreter.interpret(parser.parse("list copy size"))) == str(SelfInteger(0))
	assert str(interpreter.interpret(parser.parse("list copy isEmpty"))) == str(SelfBoolean(True))
	assert str(interpreter.interpret(parser.parse("(list copy add: 1) isEmpty"))) == str(SelfBoolean(False))

def test_list_adding_accessing_simple(interpreter : Interpreter):
	parser = Parser()
	interpreter.interpret(parser.parse("_AddSlots: (| test_list = list copy|)"))
	interpreter.interpret(parser.parse("(test_list addLast: 3) addFirst: 2"))

	assert str(interpreter.interpret(parser.parse("test_list first"))) == str(SelfInteger(2))
	assert str(interpreter.interpret(parser.parse("test_list last"))) == str(SelfInteger(3))
	assert str(interpreter.interpret(parser.parse("test_list at: 1 IfAbsent: [-1]"))) == str(SelfInteger(3))

def test_list_add_all(interpreter : Interpreter): 
	parser = Parser()
	interpreter.interpret(parser.parse("_AddSlots: (| test_list = list copy|)"))
	interpreter.interpret(parser.parse("((((test_list add: 0) add: 1) add: 2) add: 3) add: 4"))

	assert str(interpreter.interpret(parser.parse("test_list first"))) == str(SelfInteger(0))
	assert str(interpreter.interpret(parser.parse("test_list last"))) == str(SelfInteger(4))
	assert str(interpreter.interpret(parser.parse("test_list at: 1 IfAbsent: [-1]"))) == str(SelfInteger(1))

def test_list_first_link_satisfying(interpreter : Interpreter): 
	parser = Parser()
	interpreter.interpret(parser.parse("_AddSlots: (| test_list = list copy|)"))
	interpreter.interpret(parser.parse("((((test_list add: 0) add: 1) add: 2) add: 3) add: 4"))

	assert str(interpreter.interpret(parser.parse("test_list firstLinkFor: 2 IfPresent: [| :link | link value] IfAbsent: [-1]"))) == str(SelfInteger(2))
	assert str(interpreter.interpret(parser.parse("test_list firstLinkSatisfying: [| :lonk | lonk value > 2] IfPresent: [| :link | link value] IfAbsent: [-1]"))) == str(SelfInteger(3))
	assert str(interpreter.interpret(parser.parse("test_list firstLinkSatisfying: [| :lonk | lonk value > 4] IfPresent: [| :link | link value] IfAbsent: [-1]"))) == str(SelfInteger(-1))

def test_list_iteration(interpreter : Interpreter): 
	parser = Parser()
	interpreter.interpret(parser.parse("_AddSlots: (| acc <- 0. itr <- 1|)"))
	interpreter.interpret(parser.parse("_AddSlots: (| test_list = list copy|)"))
	interpreter.interpret(parser.parse("((((test_list add: 0) add: 1) add: 2) add: 3) add: 4"))
	
	assert str(interpreter.interpret(parser.parse("test_list do: [| :val | acc: acc + (val * itr). itr: itr * 10]. acc"))) == str(SelfInteger(43210))
	assert str(interpreter.interpret(parser.parse("acc: 0. itr: 1. test_list reverseDo: [| :val | acc: acc + (val * itr). itr: itr * 10]. acc"))) == str(SelfInteger(1234))
	assert str(interpreter.interpret(parser.parse("acc: 0. itr: 1. test_list with: test_list Do: [| :val1. :val2 | acc: acc + ((val1 + val2) * itr). itr: itr * 10]. acc"))) == str(SelfInteger(86420))
	assert str(interpreter.interpret(parser.parse("acc: 0. itr: 1. test_list with: test_list ReverseDo: [| :val1. :val2 | acc: acc + ((val1 + val2) * itr). itr: itr * 10]. acc"))) == str(SelfInteger(2468))
	assert str(interpreter.interpret(parser.parse("acc: 0. itr: 1. test_list doFirst: [] Middle: [| :val | acc: acc + (val * itr). itr: itr * 10] Last: [] IfEmpty: [acc: -1]. acc") )) == str(SelfInteger(321))
	assert str(interpreter.interpret(parser.parse("acc: 0. itr: 1. list copy doFirst: [] Middle: [| :val | acc: acc + (val * itr). itr: itr * 10] Last: [] IfEmpty: [acc: -1]. acc") )) == str(SelfInteger(-1))

def test_list_insertion_removal(interpreter : Interpreter):
	parser = Parser()
	interpreter.interpret(parser.parse("_AddSlots: (| test_list = list copy|)"))
	interpreter.interpret(parser.parse("((((test_list add: 0) add: 1) add: 2) add: 3) add: 4"))

	assert str(interpreter.interpret(parser.parse("test_list remove: 2 IfAbsent: [^-1]. test_list at: 2 IfAbsent: [-1]"))) == str(SelfInteger(3))
	assert str(interpreter.interpret(parser.parse("test_list insert: 2 AfterElementSatisfying: [| :val | val == 1] IfAbsent: [^-1]. test_list at: 2 IfAbsent: [-1]"))) == str(SelfInteger(2))
	assert str(interpreter.interpret(parser.parse("test_list removeFirst. test_list size"))) == str(SelfInteger(4))
	assert str(interpreter.interpret(parser.parse("test_list removeLast. test_list size"))) == str(SelfInteger(3))
	assert str(interpreter.interpret(parser.parse("acc: 0. itr: 1. test_list reverseDo: [| :val | acc: acc + (val * itr). itr: itr * 10]. acc"))) == str(SelfInteger(123))
