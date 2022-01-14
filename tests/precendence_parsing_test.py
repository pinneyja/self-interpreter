from parsing.Parser import *
from parsing.nodes.CodeNode import *
from parsing.nodes.message_nodes.UnaryMessageNode import *
from parsing.nodes.message_nodes.BinaryMessageNode import *
from parsing.nodes.message_nodes.KeywordMessageNode import *
from parsing.nodes.slot_nodes.ArgumentSlotNode import *
from parsing.nodes.slot_nodes.DataSlotNode import *
from parsing.nodes.slot_nodes.BinarySlotNode import *
from parsing.nodes.slot_nodes.KeywordSlotNode import *
from parsing.nodes.object_nodes.IntegerNode import *
from parsing.nodes.object_nodes.RegularObjectNode import *


def test_parses_all_left_right():
	parser = Parser()

	keywordObjectSlotList = [DataSlotNode("o", "=", IntegerNode(55))]
	keywordObject = RegularObjectNode(keywordObjectSlotList, CodeNode([UnaryMessageNode(None, "b")]))
	keywordSlotList = [KeywordSlotNode(["s:", "D:"], keywordObject, ["a", "b"])]
	keywordExpression = RegularObjectNode(keywordSlotList)
	middleExpression = RegularObjectNode([ArgumentSlotNode("arg")], CodeNode([keywordExpression]))
	binarySlotList = [BinarySlotNode("+", middleExpression, None)]
	binaryExpression = RegularObjectNode(binarySlotList)
	unaryReceiverSlotList = [DataSlotNode("x", "=", binaryExpression)]
	unaryReceiver = RegularObjectNode(unaryReceiverSlotList)
	unaryMessage = UnaryMessageNode(unaryReceiver, "x")
	binaryMessage = BinaryMessageNode(unaryMessage, "+", IntegerNode(3))
	keywordMessage = CodeNode([KeywordMessageNode(binaryMessage, ["s:", "D:"], [IntegerNode(1), IntegerNode(88)])])

	parserNode = parser.parse("(| x = (| + = (|:arg| (| s: a D: b = (| o = 55 | b) |) ) |) |) x + 3 s: 1 D: 88")

	generatedNodeString = str(keywordMessage)
	parserNodeString = str(parserNode)
	assert generatedNodeString == parserNodeString

def test_parses_unary_before_binary():
	parser = Parser()
	
	binarySlotExpression = RegularObjectNode([ArgumentSlotNode("arg")], CodeNode([RegularObjectNode([DataSlotNode("x", "=", IntegerNode(2))])]))
	leftHandSlots = [BinarySlotNode("+", binarySlotExpression, None)]
	leftHandSide = RegularObjectNode(leftHandSlots)

	rightHandSlots = [DataSlotNode("y", "=", IntegerNode(2)), DataSlotNode("x", "=", IntegerNode(3))]
	rightHandSide = RegularObjectNode(rightHandSlots)
	unaryMessage = UnaryMessageNode(rightHandSide, "y")
	binaryMessage = CodeNode([BinaryMessageNode(leftHandSide, "+", unaryMessage)])

	parserNode = parser.parse("(| + = (| :arg | (|x=2|) ) |) + (| y = 2. x = 3 |) y")

	generatedNodeString = str(binaryMessage)
	parserNodeString = str(parserNode)
	assert generatedNodeString == parserNodeString

def test_parses_unary_before_keyword():
	parser = Parser()

	keywordObject = RegularObjectNode([DataSlotNode("o", "=", IntegerNode(3))], CodeNode([IntegerNode(8)]))
	keywordSlotList = [KeywordSlotNode(["x:", "Y:"], keywordObject, ["a", "b"])]
	leftHandSide = RegularObjectNode(keywordSlotList)

	rightHandObject = RegularObjectNode([DataSlotNode("o", "=", IntegerNode(5))])
	rightHandSide = UnaryMessageNode(rightHandObject, "o")
	keywordMessage = CodeNode([KeywordMessageNode(leftHandSide, ["x:", "Y:"], [IntegerNode(2), rightHandSide])])

	parserNode = parser.parse("(| x: a Y: b = (| o = 3| 8) |) x: 2 Y: (| o = 5 |) o")

	generatedNodeString = str(keywordMessage)
	parserNodeString = str(parserNode)
	assert generatedNodeString == parserNodeString

def test_parses_binary_before_keyword():
	parser = Parser()

	keywordObject = RegularObjectNode([DataSlotNode("o", "=", IntegerNode(3))], CodeNode([IntegerNode(8)]))
	keywordSlotList = [KeywordSlotNode(["x:", "Y:"], keywordObject, ["a", "b"])]
	leftHandSide = RegularObjectNode(keywordSlotList)

	binarySlotExpression = RegularObjectNode([ArgumentSlotNode("arg")], CodeNode([IntegerNode(5)]))
	rightHandObject = RegularObjectNode([BinarySlotNode("+", binarySlotExpression, None)])
	rightHandSide = BinaryMessageNode(rightHandObject, "+", IntegerNode(4))
	keywordMessage = CodeNode([KeywordMessageNode(leftHandSide, ["x:", "Y:"], [IntegerNode(2), rightHandSide])])

	parserNode = parser.parse("(| x: a Y: b = (| o = 3| 8) |) x: 2 Y: (| + = (|:arg| 5) |) + 4")

	generatedNodeString = str(keywordMessage)
	parserNodeString = str(parserNode)
	assert generatedNodeString == parserNodeString

def test_parses_with_parenthesis():
	parser = Parser()

	keywordObject = RegularObjectNode([DataSlotNode("o", "=", IntegerNode(3))], CodeNode([IntegerNode(8)]))
	keywordSlotList = [KeywordSlotNode(["x:", "Y:"], keywordObject, ["a", "b"])]
	leftHandSide = RegularObjectNode(keywordSlotList)

	innerKeywordMessage = KeywordMessageNode(IntegerNode(2), ["b:", "C:"], [IntegerNode(3), IntegerNode(4)])
	keywordMessage = CodeNode([KeywordMessageNode(IntegerNode(1), ["a:"], [innerKeywordMessage])])

	innerKeywordMessageWithParentheses = KeywordMessageNode(IntegerNode(2), ["b:"], [IntegerNode(3)])
	keywordMessageWithParentheses = CodeNode([KeywordMessageNode(IntegerNode(1), ["a:", "C:"], [innerKeywordMessageWithParentheses, IntegerNode(4)])])

	parserNode = parser.parse("1 a: 2 b: 3 C: 4")
	parserNodeWithParentheses = parser.parse("1 a: (2 b: 3) C: 4")

	generatedNodeString = str(keywordMessage)
	parserNodeString = str(parserNode)
	assert generatedNodeString == parserNodeString

	generatedNodeStringWithParentheses = str(keywordMessageWithParentheses)
	parserNodeStringWithParentheses = str(parserNodeWithParentheses)
	assert generatedNodeStringWithParentheses == parserNodeStringWithParentheses

def test_binary_and_unary_message_precedence():
	parser = Parser()

	unary_message_node1 = UnaryMessageNode(IntegerNode(1), "m1")
	unary_message_node2 = UnaryMessageNode(IntegerNode(2), "m2")
	binary_message = CodeNode([BinaryMessageNode(unary_message_node1, "+", unary_message_node2)])
	parsed_object = parser.parse("1 m1 + 2 m2")

	assert str(binary_message) == str(parsed_object)

def test_assignment_has_higher_precedence_than_unary():
	parser = Parser()

	unary_message_node = UnaryMessageNode(UnaryMessageNode(None, "m1"), "m2")
	object_node = CodeNode([RegularObjectNode([DataSlotNode("x", "=", unary_message_node)])])
	parsed_object = parser.parse("(| x = m1 m2 |)")

	assert str(object_node) == str(parsed_object)

def test_assignment_has_higher_precedence_than_binary():
	parser = Parser()

	binary_message_node = BinaryMessageNode(IntegerNode(1), "+", IntegerNode(2))
	object_node = CodeNode([RegularObjectNode([DataSlotNode("x", "=", binary_message_node)])])
	parsed_object = parser.parse("(| x = 1 + 2 |)")

	assert str(object_node) == str(parsed_object)

def test_assignment_has_higher_precedence_than_keyword():
	parser = Parser()

	keyword_message_node = KeywordMessageNode(IntegerNode(1), ["m:"], [IntegerNode(2)])
	object_node = CodeNode([RegularObjectNode([DataSlotNode("x", "=", keyword_message_node)])])
	parsed_object = parser.parse("(| x = 1 m: 2 |)")

	assert str(object_node) == str(parsed_object)

def test_keyword_has_higher_precedence_than_equal_operator():
	parser = Parser()

	binary_message_node = BinaryMessageNode(IntegerNode(1), '=', IntegerNode(2))
	keyword_message_node = CodeNode([KeywordMessageNode(binary_message_node, ["ifTrue:"], [IntegerNode(3)])])
	parsed_object = parser.parse("1 = 2 ifTrue: 3")

	assert str(keyword_message_node) == str(parsed_object)

def test_keyword_has_higher_precedence_than_larrow_operator():
	parser = Parser()

	binary_message_node = BinaryMessageNode(IntegerNode(1), '<-', IntegerNode(2))
	keyword_message_node = CodeNode([KeywordMessageNode(binary_message_node, ["ifTrue:"], [IntegerNode(3)])])
	parsed_object = parser.parse("1 <- 2 ifTrue: 3")

	assert str(keyword_message_node) == str(parsed_object)