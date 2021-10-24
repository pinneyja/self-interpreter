from parsing.Parser import *
from Messages import *

def test_bad_integer_bases():
	parser = Parser()
	try:
		parser.parse("0r0")
		parser.parse("1r0")
		parser.parse("37r0")
		assert False
	except SelfParsingError as self_parsing_error:
		assert str(self_parsing_error) == Messages.INVALID_BASE.value
	
def test_bad_integer_digits():
	parser = Parser()
	for base in range(2, 10):
		for uni in range(ord('0') + base, ord('0') + 10):
			try:
				number_str = "{}r{}".format(base, chr(uni))
				print(number_str)
				parser.parse(number_str)
				assert False
			except SelfParsingError as exception:
				assert str(exception) == Messages.INVALID_DIGIT.value.format(chr(uni), base)
		for uni in range(ord('A'), ord('Z') + 1):
			try:
				number_str = "{}r{}".format(base, chr(uni))
				parser.parse(number_str)
				number_str = "{}r{}".format(base, chr(uni + 20))
				parser.parse(number_str)
				assert False
			except SelfParsingError as exception:
				assert str(exception) == Messages.INVALID_DIGIT.value.format(chr(uni), base)
	for base in range(11, 37):
		for uni in range(ord('A') + base - 10, ord('Z') + 1):
			try:
				number_str = "{}r{}".format(base, chr(uni))
				parser.parse(number_str)
				number_str = "{}r{}".format(base, chr(uni + 20))
				parser.parse(number_str)
				assert False
			except SelfParsingError as exception:
				assert str(exception) == Messages.INVALID_DIGIT.value.format(chr(uni), base)

def test_negative_with_base():
	parser = Parser()

	expected_node = CodeNode([IntegerNode(-1)])
	parsed_node = parser.parse("-2r1")
	assert str(expected_node) == str(parsed_node)

	parsed_node = parser.parse("-10r1")
	assert str(expected_node) == str(parsed_node)

	parsed_node = parser.parse("-36r1")
	assert str(expected_node) == str(parsed_node)

def test_case_sensitivity():
	parser = Parser()

	expected_node = CodeNode([IntegerNode(1)])
	parsed_node_lower = parser.parse("10r1")
	parsed_node_upper = parser.parse("10R1")
	assert str(expected_node) == str(parsed_node_lower)
	assert str(expected_node) == str(parsed_node_upper)

	expected_node = CodeNode([RealNode(100.0)])
	parsed_node_lower = parser.parse("10e1")
	parsed_node_upper = parser.parse("10E1")
	assert str(expected_node) == str(parsed_node_lower)
	assert str(expected_node) == str(parsed_node_upper)

def test_float_overflow():
	parser = Parser()

	expected_node = CodeNode([RealNode(float("inf"))])
	parsed_node = parser.parse("10e1000")
	assert str(expected_node) == str(parsed_node)

	expected_node = CodeNode([RealNode(float("-inf"))])
	parsed_node = parser.parse("-10e1000")
	assert str(expected_node) == str(parsed_node)

def test_regular_float():
	parser = Parser()

	expected_node = CodeNode([RealNode(12.0)])
	parsed_node = parser.parse("1.2e1")
	assert str(expected_node) == str(parsed_node)

	expected_node = CodeNode([RealNode(-12.0)])
	parsed_node = parser.parse("-1.2e1")
	assert str(expected_node) == str(parsed_node)

	expected_node = CodeNode([RealNode(120.0)])
	parsed_node = parser.parse("1.2e+2")
	assert str(expected_node) == str(parsed_node)

	expected_node = CodeNode([RealNode(1.2)])
	parsed_node = parser.parse("12e-1")
	assert str(expected_node) == str(parsed_node)

	expected_node = CodeNode([RealNode(0.00000000122)])
	parsed_node = parser.parse("12.2e-10")
	assert str(expected_node) == str(parsed_node)