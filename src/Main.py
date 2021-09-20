from interpreting.Interpreter import *
from parsing.Parser import *


def main():
	parser = Parser()
	interpreter = Interpreter()
	while True:
		try:
			s = input('>>> ')
		except EOFError:
			break
		print(interpreter.interpret(parser.parse(s)))

main()