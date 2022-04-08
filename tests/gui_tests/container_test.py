from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfString import SelfString
from parsing.Parser import Parser

def test_container_orientation(interpreter):
	parser = Parser()

	original_orientation_vertical = interpreter.interpret(parser.parse("container orientationIsVertical"))
	interpreter.interpret(parser.parse("container setOrientationIsVertical: false"))
	new_orientation = interpreter.interpret(parser.parse("container orientation"))

	assert str(SelfBoolean(True)) == str(original_orientation_vertical)
	assert str(SelfString("horizontal")) == str(new_orientation)

def test_container_inheritance(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("container addWidget: button"))
	button_parent_is_container = interpreter.interpret(parser.parse("button gui_parent == container"))
	assert str(SelfBoolean(True)) == str(button_parent_is_container)

	interpreter.interpret(parser.parse("container removeWidget: button"))
	button_parent_is_nil = interpreter.interpret(parser.parse("button gui_parent == nil"))
	assert str(SelfBoolean(True)) == str(button_parent_is_nil)
