from interpreting.Interpreter import *
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger

def test_nested_slot_and_object_annotations():
	# (| {} = 'obj1' {'s1' x = 1 {'s2' y = 2}} z = 3|)
	interpreter = Interpreter()
	reg_object = CodeNode([RegularObjectNode(
		object_annotation=StringNode('obj1'), 
		slot_list_annotated=[
			DataSlotNode('x', '=', IntegerNode(1), ['s1']),
			DataSlotNode('y', '=', IntegerNode(2), ['s1', 's2']),
			DataSlotNode('z', '=', IntegerNode(3)),
			]
		)])
	interpreted_result = interpreter.interpret(reg_object)
	expected_result = SelfObject({
		'x' : SelfSlot('x', SelfInteger(1), is_immutable=True, annotations=['s1']),
		'y' : SelfSlot('y', SelfInteger(2), is_immutable=True, annotations=['s1', 's2']),
		'z' : SelfSlot('z', SelfInteger(3), is_immutable=True)
	}, annotation='obj1')

	assert str(interpreted_result) == str(expected_result)

def test_nested_parallel_slot_and_object_annotations():
	# (| {} = 'obj1' {'s1' x = 1 {'s2' y = 2} {'s3' d = 4}} z = 3|)
	interpreter = Interpreter()
	reg_object = CodeNode([RegularObjectNode(
		object_annotation=StringNode('obj1'), 
		slot_list_annotated=[
			DataSlotNode('x', '=', IntegerNode(1), ['s1']),
			DataSlotNode('y', '=', IntegerNode(2), ['s1', 's2']),
			DataSlotNode('d', '=', IntegerNode(4), ['s1', 's3']),
			DataSlotNode('z', '=', IntegerNode(3)),
			]
		)])
	interpreted_result = interpreter.interpret(reg_object)
	expected_result = SelfObject({
		'x' : SelfSlot('x', SelfInteger(1), is_immutable=True, annotations=['s1']),
		'y' : SelfSlot('y', SelfInteger(2), is_immutable=True, annotations=['s1', 's2']),
		'd' : SelfSlot('d', SelfInteger(4), is_immutable=True, annotations=['s1', 's3']),
		'z' : SelfSlot('z', SelfInteger(3), is_immutable=True)
	}, annotation='obj1')

	assert str(interpreted_result) == str(expected_result)