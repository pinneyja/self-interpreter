import random
from parsing.Parser import *
from parsing.nodes.IntegerNode import *


def test_parses_random_number():
	parser = Parser()

	for i in range(100):
		number = random.randint(-9999999, 9999999)

		node = IntegerNode(number)
		parserNode = parser.parse(str(number))

		generatedNodeString = str(node)
		parserNodeString = str(parserNode)
		assert generatedNodeString == parserNodeString