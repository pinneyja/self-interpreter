from interpreting.objects.SelfInteger import SelfInteger
from .Node import Node
from parsing.SelfParsingError import *
from Messages import *
import re

class IntegerNode(Node):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def __str__(self):
		return "Integer: ('{}')".format(self.value)

	def interpret(self, context):
		return SelfInteger(self.value)
	
	def verify_syntax(self):
		tokens = re.split('[rR]', self.value, 1)
		if (len(tokens) == 1):
			self.value = int(self.value)
		else:
			base = abs(int(tokens[0]))
			digits = tokens[1]

			if (base < 2 or base > 36):
				raise SelfParsingError(Messages.INVALID_BASE.value)
			if (base <= 10):
				for digit in digits:
					if (ord(digit) >= ord('0') + base):
						raise SelfParsingError(Messages.INVALID_DIGIT.value.format(digit, base))
			else:
				for digit in digits:
					if (not (
						(ord(digit) < ord('0') + 10) or
						(ord(digit) >= ord('A') and
						ord(digit) < ord('A') + base - 10) or
						(ord(digit) >= ord('a') and
						ord(digit) < ord('a') + base - 10))):
						raise SelfParsingError(Messages.INVALID_DIGIT.value.format(digit, base))
			
			if (tokens[0].startswith('-')):
				self.value = int('-' + digits, base)
			else:
				self.value = int(digits, base)