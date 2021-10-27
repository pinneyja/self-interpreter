from parsing.Parser import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
from parsing.nodes.IntegerNode import *


def test_parses_empty_object_comment():
	parser = Parser()

	empty_object = CodeNode([RegularObjectNode()])
	parsed_empty = parser.parse("(\" I am a comment that contains lots of characters \n and you ignore me! \t \r \")")
	parsed_empty_pipe = parser.parse("(|\" I am a comment that contains lots of characters \n and you ignore me! \t \r \"|)")
	
	assert str(empty_object) == str(parsed_empty)
	assert str(empty_object) == str(parsed_empty_pipe)

def test_parses_one_number_slot_comment():
	parser = Parser()

	one_slot_obj = CodeNode([RegularObjectNode([DataSlotNode("x")])])
	one_slot_obj_equal = CodeNode([RegularObjectNode([DataSlotNode("x","=",IntegerNode(5))])])
	one_slot_obj_larrow = CodeNode([RegularObjectNode([DataSlotNode("x","<-",IntegerNode(5))])])

	parsed_one_slot_obj = parser.parse("(\"comment in weird|| spot\"|x\"another comment right up here\"|)")
	parsed_one_slot_obj_dot = parser.parse("(|x\"comments\".\"every\"|)\"where!\"")
	parsed_one_slot_obj_equal = parser.parse("(|x=5|)")
	parsed_one_slot_obj_equal_dot = parser.parse("(|x=5.|)")
	parsed_one_slot_obj_larrow = parser.parse("(|x\"<-\"<-\"you're just gonna ignore me?\"5|)")
	parsed_one_slot_obj_larrow_dot = parser.parse("\" don't mind me, just hanging out \" (|x<-5.|)")

	assert str(parsed_one_slot_obj) == str(one_slot_obj)
	assert str(parsed_one_slot_obj_dot) == str(one_slot_obj)
	assert str(parsed_one_slot_obj_equal) == str(one_slot_obj_equal)
	assert str(parsed_one_slot_obj_equal_dot) == str(one_slot_obj_equal)
	assert str(parsed_one_slot_obj_larrow) == str(one_slot_obj_larrow)
	assert str(parsed_one_slot_obj_larrow_dot) == str(one_slot_obj_larrow)

def test_parses_multiple_number_slot_comment():
	parser = Parser()

	slot_obj_equal = CodeNode([RegularObjectNode([DataSlotNode("x","=",IntegerNode(5)), DataSlotNode("y","=",IntegerNode(6))])])
	slot_obj_larrow = CodeNode([RegularObjectNode([DataSlotNode("x","<-",IntegerNode(5)), DataSlotNode("y","<-",IntegerNode(6))])])

	parsed_slot_obj_equal = parser.parse("\"I'm at beginning\"(|x=5.\"code be like /18049823)(*&#($&)Q(@)$_)!((#``,.,ncmvxnksd)) ***...|||\"y=6.|)")
	parsed_slot_obj_larrow = parser.parse("(|x<-5.\"with the power of comments, you too can write meaningless code anywhere! \n even on new lines!\" y<-6|)")

	assert str(parsed_slot_obj_equal) == str(slot_obj_equal)
	assert str(parsed_slot_obj_larrow) == str(slot_obj_larrow)

def test_nested_object_slot_comment():
	parser = Parser()

	slot_obj_equal_empty = CodeNode([RegularObjectNode([DataSlotNode("x","=",RegularObjectNode())])])
	slot_obj_larrow_nested = CodeNode([RegularObjectNode([DataSlotNode("y","<-",RegularObjectNode([DataSlotNode("x","=",IntegerNode(5)), DataSlotNode("z","=",IntegerNode(6))]))])])

	parsed_slot_obj_equal_empty = parser.parse("(|x=(\"to be or not to be\")\" that is the question\"|)\"...\"")
	parsed_slot_obj_larrow_nested = parser.parse("(|y\"you can write 'me anywhere\"<-(|x=\"even in places \n \t\t\t that don't \r \\ make // sense\"5. z=6|)|)")

	assert str(slot_obj_equal_empty) == str(parsed_slot_obj_equal_empty)
	assert str(slot_obj_larrow_nested) == str(parsed_slot_obj_larrow_nested)

def test_no_inner_quotes_allowed():
	parser = Parser()

	slot_obj_equal_empty = CodeNode([RegularObjectNode([DataSlotNode("x","=",RegularObjectNode())])])

	try:
		parsed_slot_obj_equal_empty = parser.parse("(|x=(\"\"to be or not to be\")\" that is the question\"|)\"...\"")
		assert False
	except:
		assert True