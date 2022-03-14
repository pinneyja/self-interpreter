def handleAddSlots(receiver, argument_list):
	slot_container_object = argument_list[0]
	receiver.slots.update(slot_container_object.slots)
	receiver.parent_slots.update(slot_container_object.parent_slots)
	return receiver

def handleRemoveSlot(receiver, argument_list):
	slot_name = argument_list[0].get_value()
	if slot_name in receiver.slots:
		del receiver.slots[slot_name]
	elif slot_name in receiver.parent_slots:
		del receiver.parent_slots[slot_name]
	return receiver
	
def handleAssignment(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from interpreting.objects.SelfException import SelfException
	from Messages import Messages

	if type(argument_list[0]) is not SelfString:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format("_Assignment:Value:", receiver, argument_list))

	slot_name = argument_list[0].get_value()
	value = argument_list[1]
	receiver.set_slot(slot_name, value)
	return receiver

def handleEq(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	from interpreting.primitive_methods.SmallIntPrimitives import handleIntEQ
	from interpreting.primitive_methods.SmallIntPrimitives import handleIntIfFail
	from interpreting.primitive_methods.FloatPrimitives import handleFloatEQ
	from interpreting.objects.primitive_objects.SelfString import SelfString

	if type(receiver) != type(argument_list[0]):
		return SelfBoolean(False)
	elif type(receiver) is SelfInteger:
		return handleIntIfFail(receiver, argument_list, handleIntEQ, '_Eq:')
	elif type(receiver) is SelfString:
		return SelfBoolean(str(receiver) == str(argument_list[0]))
	elif type(receiver) is SelfFloat:
		return handleFloatEQ(receiver, argument_list[0])
	else:
		return SelfBoolean(receiver == argument_list[0])

def handleRunScript(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfLobby import SelfLobby
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from interpreting.objects.SelfException import SelfException
	from Messages import Messages
	from interpreting.Interpreter import Interpreter
	from parsing.SelfParsingError import SelfParsingError
	from parsing.Parser import Parser
	import re

	if type(receiver) is not SelfString:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format("_RunScript", receiver, argument_list))

	parser = Parser()
	interpreter = Interpreter(SelfLobby.get_lobby())
	try:
		with open(receiver.get_value(), 'r') as script_file:
			file_contents = script_file.read().strip()
			file_lines = re.split('\n', file_contents)

			file_line_index = 0
			current_expression = ""
			start_new_expression = False
			number_of_lines = len(file_lines)
			while file_line_index < number_of_lines:
				if start_new_expression:
					current_expression = file_lines[file_line_index]
				else:
					current_expression += " " + file_lines[file_line_index]
					start_new_expression = True
				try:
					parsed_result = parser.parse(current_expression)
					interpreted_result = interpreter.interpret(parsed_result)
				except SelfParsingError as selfParsingError:
					if (file_line_index + 1) == number_of_lines:
						raise selfParsingError
					else:
						start_new_expression = False
				file_line_index += 1
			return interpreted_result
	except FileNotFoundError:
		raise SelfException(Messages.FILE_NOT_FOUND.value.format(receiver.get_value()))

def handleRunScriptIfFail(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.SelfObject import SelfObject

	try:
		return handleRunScript(receiver, argument_list[:-1])
	except SelfException as selfException:
		if type(argument_list[0]) is SelfObject:
			return argument_list[0].pass_unary_message("value")
		else:
			raise selfException

def handleIdentityHash(receiver, argument_list=None):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return SelfInteger(hash(receiver))

def handleIsString(receiver, argument_list=None):
	from interpreting.objects.primitive_objects.SelfString import SelfString

	if type(receiver) is not SelfString:
		return argument_list[0].pass_unary_message("value")
	else:
		return receiver

def handleClone(receiver, argument_list=None):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from interpreting.objects.primitive_objects.SelfString import SelfString

	if type(receiver) == SelfInteger or type(receiver) == SelfFloat or type(receiver) == SelfString:
		return receiver

	return receiver.clone()

def handleDefine(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from interpreting.objects.SelfException import SelfException
	from Messages import Messages
	if type(receiver) is SelfInteger or type(argument_list[0]) is SelfInteger:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_Define:'))
	if type(receiver) is SelfFloat or type(argument_list[0]) is SelfFloat:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_Define:'))
	receiver.copy_slots_of(argument_list[0])
	return receiver

def handleGetSlot(receiver, argument_list):
	from interpreting.objects.SelfSlot import SelfSlot
	from interpreting.objects.SelfObject import SelfObject
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from interpreting.objects.SelfException import SelfException
	from Messages import Messages

	if type(argument_list[0]) is not SelfString:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format("_GetSlot:", receiver, argument_list))

	slot = argument_list[0].get_value()
	if slot in receiver.slots:
		return receiver.slots[slot].value
	elif slot in receiver.parent_slots:
		return receiver.parent_slots[slot].value
	else:
		receiver.slots[slot] = SelfSlot(slot, SelfObject())
		return receiver.slots[slot].value

def handleCurrentTimeString(receiver, argument_list):
	import time
	from interpreting.objects.primitive_objects.SelfString import SelfString
	return SelfString(str(time.localtime()))

def handleThrowError(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from interpreting.objects.SelfException import SelfException
	from interpreting.printingutils.SelfObjectPrinter import SelfObjectPrinter
	from Messages import Messages

	if type(receiver) is SelfString:
		if argument_list[0].get_value() == "cannot modify an immutable string":
			raise SelfException(Messages.IMMUTABLE_ERROR.value)

	printer = SelfObjectPrinter.instance()
	error_message = printer.get_object_string(argument_list[0])
	raise SelfException(Messages.GENERIC_ERROR.value.format(error_message))

def handlePrint(receiver, argument_list=None):
	from interpreting.printingutils.SelfObjectPrinter import SelfObjectPrinter
	printer = SelfObjectPrinter.instance()
	print(printer.get_object_string(receiver))
	return receiver