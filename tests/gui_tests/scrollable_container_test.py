from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from parsing.Parser import Parser

def test_scrollable_container_inheritance(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("scrollableContainer addWidget: button"))
	button_parent_is_scrollable_container = interpreter.interpret(parser.parse("button gui_parent == scrollableContainer"))
	widgets_size_add = interpreter.interpret(parser.parse("scrollableContainer widgets size"))
	assert str(SelfBoolean(True)) == str(button_parent_is_scrollable_container)
	assert str(SelfInteger(1)) == str(widgets_size_add)

	interpreter.interpret(parser.parse("scrollableContainer removeWidget: button"))
	button_parent_is_nil = interpreter.interpret(parser.parse("button gui_parent == nil"))
	widgets_size_remove = interpreter.interpret(parser.parse("scrollableContainer widgets size"))
	assert str(SelfBoolean(True)) == str(button_parent_is_nil)
	assert str(SelfInteger(0)) == str(widgets_size_remove)	