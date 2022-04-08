from interpreting.objects.primitive_objects.SelfString import SelfString
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
from parsing.Parser import Parser

def test_textInput_text(interpreter):
	parser = Parser()

	original_textInput_text = interpreter.interpret(parser.parse("textInput text"))
	interpreter.interpret(parser.parse("lobby _AddSlots: (| testTextInput = (textInput clone) |). lobby testTextInput"))
	expected_textInput_text = "New textInput testing text"
	actual_textInput_text = interpreter.interpret(parser.parse(f"lobby testTextInput text: 'New textInput testing text'. lobby testTextInput text"))
	original_textInput_text_updated = interpreter.interpret(parser.parse("textInput text"))

	assert str(SelfString(expected_textInput_text)) == str(actual_textInput_text)
	assert str(original_textInput_text) == str(original_textInput_text_updated)

def test_textInput_position_inheritance(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("lobby _AddSlots: (| testTextInput = (textInput clone) |). lobby testTextInput"))
	interpreter.interpret(parser.parse("testTextInput position: (|x = 0.5. y = 0.5|)."))
	newPositionX = interpreter.interpret(parser.parse("testTextInput position x."))
	newPositionY = interpreter.interpret(parser.parse("testTextInput position y."))
	originalPositionX = interpreter.interpret(parser.parse("textInput position x."))
	originalPositionY = interpreter.interpret(parser.parse("textInput position y."))

	assert str(SelfFloat(0.5)) == str(newPositionX)
	assert str(SelfFloat(0.5)) == str(newPositionY)
	assert str(SelfFloat(0.0)) == str(originalPositionX)
	assert str(SelfFloat(0.0)) == str(originalPositionY)

def test_textInput_size_inheritance(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("lobby _AddSlots: (| testTextInput = (textInput clone) |). lobby testTextInput"))
	interpreter.interpret(parser.parse("testTextInput size: (|width = 0.5. height = 0.5|)."))
	newWidth = interpreter.interpret(parser.parse("testTextInput size width."))
	newHeight = interpreter.interpret(parser.parse("testTextInput size height."))
	originalWidth = interpreter.interpret(parser.parse("textInput size width."))
	originalHeight = interpreter.interpret(parser.parse("textInput size height."))

	assert str(SelfFloat(0.5)) == str(newWidth)
	assert str(SelfFloat(0.5)) == str(newHeight)
	assert str(SelfFloat(1.0)) == str(originalWidth)
	assert str(SelfFloat(1.0)) == str(originalHeight)