from parsing.Parser import *
from Messages import *
import pytest

def test_bad_integer_bases():
	parser = Parser()

	with pytest.raises(SelfParsingError, match=Messages.INVALID_BASE.value):
		parser.parse("0r0")
	with pytest.raises(SelfParsingError, match=Messages.INVALID_BASE.value):
		parser.parse("1r0")
	with pytest.raises(SelfParsingError, match=Messages.INVALID_BASE.value):
		parser.parse("37r0")
	
def test_bad_integer_digits():
	parser = Parser()

	for base in range(2, 10):
		for uni in range(ord('0') + base, ord('0') + 10):
			# numeric digits
			number_str = "{}r{}".format(base, chr(uni))
			with pytest.raises(SelfParsingError, match=Messages.INVALID_DIGIT.value.format(chr(uni), base)):
				parser.parse(number_str)
		for uni in range(ord('A'), ord('Z') + 1):
			# uppercase digits
			number_str = "{}r{}".format(base, chr(uni))
			with pytest.raises(SelfParsingError, match=Messages.INVALID_DIGIT.value.format(chr(uni), base)):
				parser.parse(number_str)
			# lowercase digits
			number_str = "{}r{}".format(base, chr(uni + 32))
			with pytest.raises(SelfParsingError, match=Messages.INVALID_DIGIT.value.format(chr(uni + 32), base)):
				parser.parse(number_str)

	for base in range(11, 37):
		for uni in range(ord('A') + base - 10, ord('Z') + 1):
			# uppercase digits
			number_str = "{}r{}".format(base, chr(uni))
			with pytest.raises(SelfParsingError, match=Messages.INVALID_DIGIT.value.format(chr(uni), base)):
				parser.parse(number_str)
			# lowercase digits
			number_str = "{}r{}".format(base, chr(uni + 32))
			with pytest.raises(SelfParsingError, match=Messages.INVALID_DIGIT.value.format(chr(uni + 32), base)):
				parser.parse(number_str)
		

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

def test_integer_in_obj():
	parser = Parser()

	parsed_node = parser.parse("[| :x | x + x] value: 3")
	assert parsed_node.expressions[0].value_list[0].value == 3