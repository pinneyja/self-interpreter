from os import system
from interpreting.Interpreter import *
from interpreting.printingutils.SelfObjectPrinter import SelfObjectPrinter
from parsing.Parser import *
from sys import platform
import traceback
if platform == "linux":
	import readline

def main():
	isParser = False
	parser = Parser()
	interpreter = Interpreter()
	printer = SelfObjectPrinter()
	system("")

	mode = input('Select mode (i)nterpret or (p)arse: ')
	if mode == "p":
		isParser = True
	else:
		try:
			interpreter.initializeBootstrap()
		except (SelfException, SelfParsingError) as selfError:
			print(selfError)
			print(Messages.BOOTSTRAP_FAILED.value)
		except Exception:
			traceback.print_exc()
			print(Messages.BOOTSTRAP_FAILED.value)

	while True:
		try:
			s = input('>>> ')
		except EOFError:
			break

		if s.strip() == "":
			continue

		try:
			if isParser:
				print(parser.parse(s))
			else:
				print(printer.get_object_string(interpreter.interpret(parser.parse(s))))
		except (SelfParsingError, SelfException) as selfError:
			print(selfError)
		except Exception:
			traceback.print_exc()

main()