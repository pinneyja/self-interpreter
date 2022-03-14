from parsing.Parser import Parser
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean

def test_set_basic(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (|s = set copy|)"))
	actual = interpreter.interpret(parser.parse("s add: 2. s includes: 2"))
	actual2 = interpreter.interpret(parser.parse("s includes: 3"))

	assert str(SelfBoolean(True)) == str(actual)
	assert str(SelfBoolean(False)) == str(actual2)

def test_set_remove(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (|s = set copy|)"))
	actual = interpreter.interpret(parser.parse("s add: 2. s includes: 2"))
	actual2 = interpreter.interpret(parser.parse("s remove: 2. s includes: 2"))

	assert str(SelfBoolean(True)) == str(actual)
	assert str(SelfBoolean(False)) == str(actual2)

def test_set_iteration(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (|s = (1 & 2 & 3 & 4) asSet. x <- 0. |)"))
	actual = interpreter.interpret(parser.parse("s do: [|:e| x: x + e]. x"))

	assert str(SelfInteger(10)) == str(actual)

def test_set_intersect(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (|s = (1 & 2 & 3 & 4) asSet. s2 = (3 & 4 & 5 & 6) asSet |)"))
	actual = interpreter.interpret(parser.parse("(s intersect: s2) size"))

	assert str(SelfInteger(2)) == str(actual)

def test_dictionary_basic(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (|d = dictionary copy|)"))
	actual = interpreter.interpret(parser.parse("d at: 2 Put: 20. d at: 2"))
	actual2 = interpreter.interpret(parser.parse("d at: 3 IfAbsent: false"))

	assert str(SelfInteger(20)) == str(actual)
	assert str(SelfBoolean(False)) == str(actual2)

def test_dictionary_includes(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (|d = dictionary copy|)"))
	interpreter.interpret(parser.parse("d at: 1 Put: 100"))
	actual = interpreter.interpret(parser.parse("d includesKey: 1"))
	actual2 = interpreter.interpret(parser.parse("d includesKey: 100"))
	actual3 = interpreter.interpret(parser.parse("d includes: 1"))
	actual4 = interpreter.interpret(parser.parse("d includes: 100"))

	assert str(SelfBoolean(True)) == str(actual)
	assert str(SelfBoolean(False)) == str(actual2)
	assert str(SelfBoolean(False)) == str(actual3)
	assert str(SelfBoolean(True)) == str(actual4)

def test_dictionary_remove(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (|d = dictionary copy|)"))
	interpreter.interpret(parser.parse("d at: 1 Put: 1. d at: 2 Put: 2"))
	interpreter.interpret(parser.parse("d removeKey: 1"))
	actual = interpreter.interpret(parser.parse("d includesKey: 1"))
	actual2 = interpreter.interpret(parser.parse("d includesKey: 2"))

	assert str(SelfBoolean(False)) == str(actual)
	assert str(SelfBoolean(True)) == str(actual2)

def test_dictionary_iteration(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("_AddSlots: (|d = dictionary copy. x <- 0|)"))
	interpreter.interpret(parser.parse("d at: 1 Put: 100. d at: 2 Put: 200"))
	actual = interpreter.interpret(parser.parse("d do: [|:v. :k| x: x + (v+k)]. x"))

	assert str(SelfInteger(303)) == str(actual)