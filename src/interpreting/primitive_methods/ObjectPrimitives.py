def handleAddSlots(receiver, argument_list):
	slot_container_object = argument_list[0]
	receiver.slots.update(slot_container_object.slots)
	receiver.parent_slots.update(slot_container_object.parent_slots)
	return receiver
	
def handleAssignment(receiver, argument_list):
	slot_name = argument_list[0].value
	value = argument_list[1]
	receiver.set_slot(slot_name, value)
	return receiver

def handleEq(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from interpreting.objects.primitive_objects.SelfReal import SelfReal
	from interpreting.objects.primitive_objects.SelfBoolean import SelfBoolean
	from interpreting.primitive_methods.IntPrimitives import handleIntEQ
	from interpreting.primitive_methods.FloatPrimitives import handleFloatEQ

	if type(receiver) != type(argument_list[0]):
		return SelfBoolean(False)
	elif type(receiver) is SelfInteger:
		return handleIntEQ(receiver, argument_list)
	elif type(receiver) is SelfReal:
		return handleFloatEQ(receiver, argument_list)
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
		with open(receiver.value, 'r') as script_file:
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
		raise SelfException(Messages.FILE_NOT_FOUND.value.format(receiver.value))

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
	from interpreting.objects.primitive_objects.SelfReal import SelfReal
	from interpreting.objects.primitive_objects.SelfString import SelfString

	if type(receiver) == SelfInteger or type(receiver) == SelfReal or type(receiver) == SelfString:
		return receiver

	return receiver.clone()

def handleDefine(receiver, argument_list):
	from interpreting.objects.SelfObject import SelfObject
	from interpreting.objects.SelfException import SelfException
	from Messages import Messages
	if type(receiver) is not SelfObject or type(argument_list[0]) is not SelfObject:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_Define:'))
	receiver.copy_slots_of(argument_list[0])
	return receiver