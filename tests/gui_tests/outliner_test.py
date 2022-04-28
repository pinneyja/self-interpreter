from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.objects.primitive_objects.SelfString import SelfString
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from parsing.Parser import Parser

def test_add_and_remove_outliners(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("canvas removeAllWidgets"))
	interpreter.interpret(parser.parse("canvas addOutliner: 1"))
	interpreter.interpret(parser.parse("canvas addOutliner: (|x = 'test'|)"))
	num_widgets = interpreter.interpret(parser.parse("canvas widgets size"))
	interpreter.interpret(parser.parse("canvas removeWidget: (canvas widgets first)"))
	num_widgets2 = interpreter.interpret(parser.parse("canvas widgets size"))

	assert str(SelfInteger(2)) == str(num_widgets)
	assert str(SelfInteger(1)) == str(num_widgets2)

def test_outliner_contents_simple_object(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("canvas removeAllWidgets. canvas addOutliner: (|x = 1. p* = 2|)"))
	widgets_in_outliner = interpreter.interpret(parser.parse("(canvas widgets first) widgets size"))
	outliner_name = interpreter.interpret(parser.parse("(canvas widgets first) widgets first text"))
	slot_name = interpreter.interpret(parser.parse("(canvas widgets first) widgets last widgets last text"))
	slot_name2 = interpreter.interpret(parser.parse("(canvas widgets first) widgets last widgets first text"))
	interpreter.interpret(parser.parse("((canvas widgets first) widgets at: 1) widgets last onRelease"))
	num_widgets = interpreter.interpret(parser.parse("canvas widgets size"))

	assert str(SelfInteger(3)) == str(widgets_in_outliner)
	assert str(SelfString("a slots object")) == str(outliner_name)
	assert str(SelfString("x")) == str(slot_name)
	assert str(SelfString("p*")) == str(slot_name2)
	assert str(SelfInteger(0)) == str(num_widgets)

def test_outliner_pops_out_slots(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("canvas removeAllWidgets. canvas addOutliner: (|x = 1. p* = 2|)"))
	interpreter.interpret(parser.parse("(canvas widgets first) widgets last widgets first onRelease"))
	num_widgets = interpreter.interpret(parser.parse("canvas widgets size"))
	outliner_name = interpreter.interpret(parser.parse("canvas widgets last widgets first text"))
	interpreter.interpret(parser.parse("(canvas widgets first) widgets last widgets last onRelease"))
	num_widgets2 = interpreter.interpret(parser.parse("canvas widgets size"))
	outliner_name2 = interpreter.interpret(parser.parse("canvas widgets last widgets first text"))
	
	assert str(SelfInteger(2)) == str(num_widgets)
	assert str(SelfInteger(3)) == str(num_widgets2)
	assert str(SelfString("2")) == str(outliner_name)
	assert str(SelfString("1")) == str(outliner_name2)

def test_outliner_evaluator_open_and_close(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("canvas removeAllWidgets. canvas addOutliner: ()"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets at: 1) widgets first onRelease"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets at: 1) widgets first onRelease"))
	num_widgets_in_outliner = interpreter.interpret(parser.parse("canvas widgets first widgets size"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets last widgets last widgets last) onRelease"))
	num_widgets_in_outliner2 = interpreter.interpret(parser.parse("canvas widgets first widgets size"))

	assert str(SelfInteger(5)) == str(num_widgets_in_outliner)
	assert str(SelfInteger(4)) == str(num_widgets_in_outliner2)

def test_outliner_evaluator_do_it(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("canvas removeAllWidgets. canvas addOutliner: (|x <- 1. p* = 2|)"))
	num_widgets_in_outliner = interpreter.interpret(parser.parse("canvas widgets first widgets size"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets at: 1) widgets first onRelease"))
	num_widgets_in_outliner2 = interpreter.interpret(parser.parse("canvas widgets first widgets size"))
	interpreter.interpret(parser.parse("canvas widgets first widgets last widgets first text: 'x: 7'"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets last widgets last widgets at: 1) onRelease"))
	interpreter.interpret(parser.parse("((canvas widgets first widgets at: 2) widgets at: 1) onRelease"))
	outliner_name = interpreter.interpret(parser.parse("canvas widgets last widgets first text"))
		
	assert str(SelfInteger(3)) == str(num_widgets_in_outliner)
	assert str(SelfInteger(4)) == str(num_widgets_in_outliner2)
	assert str(SelfString("7")) == str(outliner_name)

def test_outliner_evaluator_get_it(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("canvas removeAllWidgets. canvas addOutliner: (|x <- 1. p* = 2|)"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets at: 1) widgets first onRelease"))
	interpreter.interpret(parser.parse("canvas widgets first widgets last widgets first text: '7'"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets last widgets last widgets first) onRelease"))
	outliner_name = interpreter.interpret(parser.parse("canvas widgets last widgets first text"))
		
	assert str(SelfString("7")) == str(outliner_name)

def test_outliner_update_method(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("lobby _AddSlots: (|x = (|m = (| | 2 + 2)|) |)"))
	interpreter.interpret(parser.parse("canvas removeAllWidgets. canvas addOutliner: x"))
	result_before = interpreter.interpret(parser.parse("x m"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets last widgets first widgets at: 1) text: '| | 3 + 4'"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets last widgets first widgets last widgets first) onRelease"))
	result_after = interpreter.interpret(parser.parse("x m"))
			
	assert str(SelfInteger(4)) == str(result_before)
	assert str(SelfInteger(7)) == str(result_after)

def test_outliner_reset_method(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("lobby _AddSlots: (|x = (|m = (| | 2 + 2)|) |)"))
	interpreter.interpret(parser.parse("canvas removeAllWidgets. canvas addOutliner: x"))
	result_before = interpreter.interpret(parser.parse("x m"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets last widgets first widgets at: 1) text: '| | 3 + 4'"))
	interpreter.interpret(parser.parse("(canvas widgets first widgets last widgets first widgets last widgets last) onRelease"))
	text_after_reset = interpreter.interpret(parser.parse("(canvas widgets first widgets last widgets first widgets at: 1) text"))
	result_after = interpreter.interpret(parser.parse("x m"))
			
	assert str(SelfInteger(4)) == str(result_before)
	assert str(SelfInteger(4)) == str(result_after)
	assert str(SelfString("| | 2 + 2")) == str(text_after_reset)

def test_outliner_for_vectors(interpreter):
	parser = Parser()

	interpreter.interpret(parser.parse("canvas removeAllWidgets. canvas addOutliner: (1 & 2 & 3) asVector"))
	num_widgets_in_outliner = interpreter.interpret(parser.parse("canvas widgets first widgets size"))
	slot_name = interpreter.interpret(parser.parse("canvas widgets first widgets last widgets last text"))
	interpreter.interpret(parser.parse("canvas widgets first widgets last widgets last onRelease"))
	outliner_name = interpreter.interpret(parser.parse("canvas widgets last widgets first text"))

	assert str(SelfInteger(5)) == str(num_widgets_in_outliner)
	assert str(SelfString("<2>")) == str(slot_name)
	assert str(SelfString("3")) == str(outliner_name)