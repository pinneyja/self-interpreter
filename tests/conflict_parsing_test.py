from parsing.Parser import *

parser_out_path = './src/parsing/parser.out'
parser = Parser()

def test_parser_has_no_shift_reduce_conflicts():
	with open(parser_out_path, 'r') as parser_file:
		file_contents = parser_file.read()
		assert ("! shift/reduce conflict" in file_contents) == False

def test_parser_has_no_reduce_reduce_conflicts():
	with open(parser_out_path, 'r') as parser_file:
		file_contents = parser_file.read()
		assert ("! reduce/reduce conflict" in file_contents) == False