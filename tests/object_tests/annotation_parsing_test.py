from parsing.Parser import *

def test_basic_object_annotation():
	parser = Parser()

	reg_object = CodeNode([RegularObjectNode(object_annotation=StringNode('obj1'))])

	parsed_object = parser.parse("(| {} = 'obj1'|)")
	assert str(reg_object) == str(parsed_object)

def test_basic_object_annotation_period():
	parser = Parser()

	reg_object = CodeNode([RegularObjectNode(object_annotation=StringNode('obj1'))])

	parsed_object = parser.parse("(| {} = 'obj1'.|)")
	assert str(reg_object) == str(parsed_object)

def test_basic_annotated_slots():
	parser = Parser()
	reg_object = CodeNode([RegularObjectNode(slot_list_annotated=[DataSlotNode('x', '=', IntegerNode(1), ['s1'])])])

	parsed_object = parser.parse("(| {'s1' x = 1} |)")
	assert str(reg_object) == str(parsed_object)

def test_intermixed_and_layered_annotations():
	parser = Parser()
	reg_object = CodeNode([RegularObjectNode(
		object_annotation=StringNode('obj1'), 
		slot_list_annotated=[
			DataSlotNode('x', '=', IntegerNode(1), ['s1']),
			DataSlotNode('y', '=', IntegerNode(2), ['s1', 's2']),
			DataSlotNode('z', '=', IntegerNode(3)),
			]
		)])

	parsed_object = parser.parse("(| {} = 'obj1' {'s1' x = 1 {'s2' y = 2}} z = 3|)")
	assert str(reg_object) == str(parsed_object)

def test_intermixed_and_layered_annotations_period():
	parser = Parser()
	reg_object = CodeNode([RegularObjectNode(
		object_annotation=StringNode('obj1'), 
		slot_list_annotated=[
			DataSlotNode('x', '=', IntegerNode(1), ['s1']),
			DataSlotNode('y', '=', IntegerNode(2), ['s1', 's2']),
			DataSlotNode('z', '=', IntegerNode(3)),
			]
		)])

	parsed_object = parser.parse("(| {} = 'obj1'. {'s1' x = 1 {'s2' y = 2}} z = 3|)")
	assert str(reg_object) == str(parsed_object)

def test_intermixed_and_layered_annotations_2():
	parser = Parser()
	reg_object = CodeNode([RegularObjectNode(
		object_annotation=StringNode('obj1'), 
		slot_list_annotated=[
			DataSlotNode('x', '=', IntegerNode(1), ['s1']),
			DataSlotNode('y', '=', IntegerNode(2), ['s1', 's2', 's4']),
			DataSlotNode('e', '=', IntegerNode(5), ['s1', 's3']),
			DataSlotNode('d', '=', IntegerNode(4), ['s1']),
			DataSlotNode('z', '=', IntegerNode(3)),
			]
		)])

	parsed_object = parser.parse("(| {} = 'obj1' {'s1' x = 1 {'s2' {'s4' y = 2}} {'s3' e = 5} d = 4} z = 3|)")
	assert str(reg_object) == str(parsed_object)