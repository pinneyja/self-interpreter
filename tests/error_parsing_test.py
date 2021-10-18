from parsing.Parser import *
from Messages import *

def test_bad_number_arg_slots_binary_slot():
	parser = Parser()

	try:
		parser.parse("(| + = (| | 5)|)")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.INVALID_NUMBER_ARG_SLOTS.value

	try:
		parser.parse("(| + = (|:arg1. :arg2| 4) |)")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.INVALID_NUMBER_ARG_SLOTS.value

def test_bad_number_arg_slots_keyword_slot():
	parser = Parser()

	try:
		parser.parse("(| id1: Id2: = (| :arg1 | 0)|)")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.INVALID_NUMBER_ARG_SLOTS.value

	try:
		parser.parse("(| id1: Id2: = (| :arg1. :arg2. :arg3 | 0)|)")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.INVALID_NUMBER_ARG_SLOTS.value

def test_bad_number_arg_slots_args_in_no_context():
	parser = Parser()

	try:
		parser.parse("(| :arg |)")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.INVALID_NUMBER_ARG_SLOTS.value

def test_empty_argument_object():
	parser = Parser()

	try:
		parser.parse("(| + = (| :arg |)|)")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.EMPTY_OBJECT_WITH_ARG.value

def test_production_error():
	parser = Parser()

	try:
		parser.parse("(")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.SYNTAX_ERROR_AT_TOKEN.value.format("None")

	try:
		parser.parse("())")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.SYNTAX_ERROR_AT_TOKEN.value.format(")")

	try:
		parser.parse("(| + = 0 |)")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.SYNTAX_ERROR_AT_TOKEN.value.format("0")

	try:
		parser.parse("(| id1: id2: = (| :arg1. :arg2 | 0)|)")
		assert False
	except SelfParsingError as exception:
		assert str(exception) == Messages.SYNTAX_ERROR_AT_TOKEN.value.format("id2:")