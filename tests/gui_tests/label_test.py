from interpreting.objects.primitive_objects.SelfString import SelfString
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
from parsing.Parser import Parser

def test_label_text(interpreter):
	parser = Parser()

	original_label_text = interpreter.interpret(parser.parse("label text"))
	interpreter.interpret(parser.parse("lobby _AddSlots: (| testLabel = (label clone) |). lobby testLabel"))
	expected_label_text = "New label testing text"
	actual_label_text = interpreter.interpret(parser.parse(f"lobby testLabel text: 'New label testing text'. lobby testLabel text"))
	original_label_text_updated = interpreter.interpret(parser.parse("label text"))

	assert str(SelfString(expected_label_text)) == str(actual_label_text)
	assert str(original_label_text) == str(original_label_text_updated)

def test_label_inheritance(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("lobby _AddSlots: (| testLabel = (label clone) |). lobby testLabel"))
	interpreter.interpret(parser.parse("testLabel position: (|x = 0.5. y = 0.5|)."))
	newPositionX = interpreter.interpret(parser.parse("testLabel position x."))
	newPositionY = interpreter.interpret(parser.parse("testLabel position y."))
	originalPositionX = interpreter.interpret(parser.parse("label position x."))
	originalPositionY = interpreter.interpret(parser.parse("label position y."))

	assert str(SelfFloat(0.5)) == str(newPositionX)
	assert str(SelfFloat(0.5)) == str(newPositionY)
	assert str(SelfFloat(0.0)) == str(originalPositionX)
	assert str(SelfFloat(0.0)) == str(originalPositionY)