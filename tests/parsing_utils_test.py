from parsing.utils.ParsingUtils import *
from parsing.SelfParsingError import *
import pytest


def test_convert_d_and_o_escapes_to_x():
	s = r'\d123\o123'
	converted = convert_d_and_o_escapes_to_x(s)
	assert converted == r'\x7b\x53'

	s = r'\d255\o377'
	converted = convert_d_and_o_escapes_to_x(s)
	assert converted == r'\xff\xff'

def test_exception_convert_d_and_o_escapes_to_x():
	s = r'\d256'
	with pytest.raises(Exception) as e:
		convert_d_and_o_escapes_to_x(s)
	assert e.type == SelfParsingError

	s = r'\o400'
	with pytest.raises(Exception) as e:
		convert_d_and_o_escapes_to_x(s)
	assert e.type == SelfParsingError

def test_remove_backslash_from_backslash_question_mark():
	s = r'abc\?def\?ghi'
	removed = remove_backslash_from_backslash_question_mark(s)
	assert removed == 'abc?def?ghi'

def test_raw_string_to_normal_string():
	s = 'test'
	converted = raw_string_to_normal_string(s)
	assert converted == 'test'

def test_raw_string_to_normal_string_with_escapes():
	s = r'\t\b\n\f\r\v\a\0\\\'\"?'
	converted = raw_string_to_normal_string(s)
	assert converted == '\t\b\n\f\r\v\a\0\\\'\"?'
	assert len(converted) == 12

def test_raw_string_to_normal_string_with_numeric_escapes():
	s = r'\xff\d255\o377'
	converted = convert_d_and_o_escapes_to_x(s)
	converted = raw_string_to_normal_string(converted)
	assert converted == '\xff\xff\xff'
	assert len(converted) == 3