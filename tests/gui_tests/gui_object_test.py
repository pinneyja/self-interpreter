from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
from parsing.Parser import Parser

def test_gui_object_position(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("lobby _AddSlots: (| testButton = (button clone) |). lobby testButton"))
	interpreter.interpret(parser.parse("testButton position: (|x = 0.5. y = 0.5|)."))
	newPositionX = interpreter.interpret(parser.parse("testButton position x."))
	newPositionY = interpreter.interpret(parser.parse("testButton position y."))
	originalPositionX = interpreter.interpret(parser.parse("button position x."))
	originalPositionY = interpreter.interpret(parser.parse("button position y."))

	assert str(SelfFloat(0.5)) == str(newPositionX)
	assert str(SelfFloat(0.5)) == str(newPositionY)
	assert str(SelfFloat(0.0)) == str(originalPositionX)
	assert str(SelfFloat(0.0)) == str(originalPositionY)

def test_gui_object_size(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("lobby _AddSlots: (| testLabel = (label clone) |). lobby testLabel"))
	interpreter.interpret(parser.parse("testLabel size: (|width = 0.5. height = 0.5|)."))
	newWidth = interpreter.interpret(parser.parse("testLabel size width."))
	newHeight = interpreter.interpret(parser.parse("testLabel size height."))
	originalWidth = interpreter.interpret(parser.parse("label size width."))
	originalHeight = interpreter.interpret(parser.parse("label size height."))

	assert str(SelfFloat(0.5)) == str(newWidth)
	assert str(SelfFloat(0.5)) == str(newHeight)
	assert str(SelfFloat(1.0)) == str(originalWidth)
	assert str(SelfFloat(1.0)) == str(originalHeight)