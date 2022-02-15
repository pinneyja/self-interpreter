from Messages import Messages
from interpreting.Interpreter import Interpreter
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.SelfException import SelfException
from parsing.Parser import Parser
import pytest

filename = "self_files/test.self"

@pytest.fixture(scope="module")
def interpreter():
	interpreter = Interpreter()
	interpreter.initializeBootstrap()
	return interpreter

def read_file():
	with open(filename, "r") as f:
		return f.read()

def write_file(contents):
	with open(filename, "w") as f:
		f.write(contents)

def script_code_helper(script_contents, expected_result, interpreter):
	file_contents = read_file()
	write_file(script_contents)

	try:
		result = interpreter.interpret(Parser().parse("'self_files/test.self' _RunScript"))
	except Exception as e:
		write_file(file_contents)
		raise e

	write_file(file_contents)

	assert str(result) == str(expected_result)

def test_basic_script():
	script_code_helper("3", SelfInteger(3), Interpreter())

def test_nested_statement_script():
	file_contents = read_file()
	write_file("x: 3. x")
	
	interpreter = Interpreter()
	parser = Parser()
	result = interpreter.interpret(parser.parse("_AddSlots: (|x <- 1|). (| sc = (| x = 2 | 'self_files/test.self' _RunScript) |) sc"))

	write_file(file_contents)

	assert str(result) == str(SelfInteger(3))

def test_multiline_script():
	script_code_helper("lobby _AddSlots: (| y <- 1 |)\ny: 3\nlobby _AddSlots: (|\nx <- 3\n|)\nx\n", SelfInteger(3), Interpreter())
	script_code_helper("lobby _AddSlots: (| y <- 1 |)\ny: 5\nlobby _AddSlots: (|\n\t\n\nx <- 3\n|)\ny\n", SelfInteger(5), Interpreter())
	script_code_helper("lobby \n_AddSlots: (| y <-\n 1 |)\n\nlobby _AddSlots: (|\n\t\n\nx <- 3\n|)\ny\n", SelfInteger(1), Interpreter())
	script_code_helper("lobby \t\n_AddSlots: (| y <- 1\n |)\ny: 5\nlobby _AddSlots: (|\n\t\n\nx <- 234\n|)\nx\n", SelfInteger(234), Interpreter())
	script_code_helper("\n\nlobby _AddSlots: \n(| y <- \n1 |)\ny: 55\nlobby _AddSlots: (|\n\t\n\nx <- 3\n|)\ny", SelfInteger(55), Interpreter())

def test_partially_executes_script():
	interpreter = Interpreter()
	try:
		script_code_helper("lobby _AddSlots: (| x <- 1 |). x: 2\nbadMessage\nx: 3", None, interpreter)
		assert False
	except SelfException as selfException:
		assert str(selfException) == str(SelfException("Lookup error, 'badMessage' not found"))
		assert str(interpreter.interpret(Parser().parse("x"))) == str(SelfInteger(2))

def test_error_no_file(interpreter):
	parser = Parser()
	filename = "nonexistantFileName"
	with pytest.raises(SelfException, match=Messages.FILE_NOT_FOUND.value.format(filename)):
		interpreter.interpret(parser.parse(f"'{filename}' _RunScript"))