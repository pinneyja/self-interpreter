from parsing.SelfParsingError import *
from Messages import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.CodeNode import *
import re
import codecs

def convert_d_and_o_escapes_to_x(s):
	pattern = r'\\(d|o)[0-9]{3}'
	match = re.search(pattern, s)
	while (match):
		if match.group(1) == 'd':
			decimalValue = int(match.group()[2:])
		else:
			decimalValue = int(match.group()[2:], 8)
		if decimalValue > 255:
			raise SelfParsingError(Messages.INVALID_ESCAPE_CHARACTER.value.format(match.group()))
		hexValue = hex(decimalValue)[2:]
		s = s.replace(match.group(), r'\x' + hexValue, 1)
		match = re.search(pattern, s)
	return s

def remove_backslash_from_backslash_question_mark(s):
	return s.replace(r'\?', '?')

def raw_string_to_normal_string(s):
	return codecs.decode(s, 'unicode_escape')

def get_first_expression_if_method(object_node):
	if type(object_node) is RegularObjectNode and object_node.code:
		expressions = object_node.code.expressions
		if len(expressions) != 1:
			raise SelfParsingError(Messages.MULTIPLE_EXPRESSIONS_IN_SUB_EXPRESSION.value)
		return expressions[0]
	else:
		return object_node