from interpreting.objects.primitive_objects.SelfString import SelfString
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
from parsing.Parser import Parser

def test_button_text(interpreter):
	parser = Parser()

	original_button_text = interpreter.interpret(parser.parse("button text"))
	interpreter.interpret(parser.parse("lobby _AddSlots: (| testButton = (button clone) |). lobby testButton"))
	expected_button_text = "New button testing text"
	actual_button_text = interpreter.interpret(parser.parse(f"lobby testButton text: 'New button testing text'. lobby testButton text"))
	original_button_text_updated = interpreter.interpret(parser.parse("button text"))

	assert str(SelfString(expected_button_text)) == str(actual_button_text)
	assert str(original_button_text) == str(original_button_text_updated)

def test_button_on_press_and_on_release(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("lobby _AddSlots: (|x <- 0 |)."))
	testButton = interpreter.interpret(parser.parse("lobby _AddSlots: (| testButton = (button clone) |). lobby testButton"))
	interpreter.interpret(parser.parse("testButton _AddSlots: (| onPress = (| | x: x + 1) |)."))
	interpreter.interpret(parser.parse("testButton _AddSlots: (| onRelease = (| | x: x + 10) |)."))
	testButton.kivy_widget.dispatch('on_press')
	testButton.kivy_widget.dispatch('on_release')
	testButton.kivy_widget.dispatch('on_press')
	actual = interpreter.interpret(parser.parse("x"))

	assert str(SelfInteger(12)) == str(actual)

def test_button_inheritance(interpreter):
	parser = Parser()

	testButton = interpreter.interpret(parser.parse("lobby _AddSlots: (| testButton = (button clone) |). lobby testButton"))
	interpreter.interpret(parser.parse("testButton size: (|width = 0.5. height = 0.5|)."))
	newWidth = interpreter.interpret(parser.parse("testButton size width."))
	newHeight = interpreter.interpret(parser.parse("testButton size height."))
	originalWidth = interpreter.interpret(parser.parse("button size width."))
	originalHeight = interpreter.interpret(parser.parse("button size height."))

	assert str(SelfFloat(0.5)) == str(newWidth)
	assert str(SelfFloat(0.5)) == str(newHeight)
	assert str(SelfFloat(1.0)) == str(originalWidth)
	assert str(SelfFloat(1.0)) == str(originalHeight)