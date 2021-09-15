from parsing.Parser import *

parser = Parser()
while True:
	try:
		s = input('>>> ')
	except EOFError:
		break
	print(parser.parse(s))