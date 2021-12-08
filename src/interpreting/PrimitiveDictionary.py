from interpreting.objects.SelfException import *
from Messages import *

def handleIntAdd(receiver, argument_list):
	from interpreting.objects.SelfInteger import SelfInteger
	argument = argument_list[0]
	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format("_IntAdd:", receiver, argument))

	return SelfInteger(receiver.get_value() + argument.get_value())

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

def handleRunScript(receiver, argument_list):
	from interpreting.objects.SelfLobby import SelfLobby
	from interpreting.objects.SelfString import SelfString
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

def handleIntComparison(receiver, argument_list, operator, primitive_name):
	from interpreting.objects.SelfBoolean import SelfBoolean
	from interpreting.objects.SelfInteger import SelfInteger
	argument = argument_list[0]
	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive_name, receiver, argument))

	int1 = receiver.get_value()
	int2 = argument.get_value()
	boolean_result = operator(int1, int2)

	return SelfBoolean(boolean_result)

def handleFloatComparison(receiver, argument_list, operator, primitive_name):
	from interpreting.objects.SelfBoolean import SelfBoolean
	from interpreting.objects.SelfReal import SelfReal
	argument = argument_list[0]
	if type(receiver) is not SelfReal or type(argument) is not SelfReal:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive_name, receiver, argument))

	float1 = receiver.get_value()
	float2 = argument.get_value()
	boolean_result = operator(float1, float2)

	return SelfBoolean(boolean_result)

def handleIntNE(receiver, argument_list):
	return handleIntComparison(receiver, argument_list, lambda x, y: x != y, "_IntNE:")

def handleIntLT(receiver, argument_list):
	return handleIntComparison(receiver, argument_list, lambda x, y: x < y, "_IntLT:")

def handleIntLE(receiver, argument_list):
	return handleIntComparison(receiver, argument_list, lambda x, y: x <= y, "_IntLE:")

def handleIntEQ(receiver, argument_list):
	return handleIntComparison(receiver, argument_list, lambda x, y: x == y, "_IntEQ:")

def handleIntGT(receiver, argument_list):
	return handleIntComparison(receiver, argument_list, lambda x, y: x > y, "_IntGT:")

def handleIntGE(receiver, argument_list):
	return handleIntComparison(receiver, argument_list, lambda x, y: x >= y, "_IntGE:")

def handleFloatEQ(receiver, argument_list):
	return handleFloatComparison(receiver, argument_list, lambda x, y: x == y, "_FloatEQ:")

def handleEq(receiver, argument_list):
	from interpreting.objects.SelfInteger import SelfInteger
	from interpreting.objects.SelfReal import SelfReal
	from interpreting.objects.SelfBoolean import SelfBoolean

	if type(receiver) != type(argument_list[0]):
		return SelfBoolean(False)
	elif type(receiver) is SelfInteger:
		return handleIntEQ(receiver, argument_list)
	elif type(receiver) is SelfReal:
		return handleFloatEQ(receiver, argument_list)
	else:
		return SelfBoolean(receiver == argument_list[0])

def handleIdentityHash(receiver, argument_list=None):
	from interpreting.objects.SelfInteger import SelfInteger
	return SelfInteger(hash(receiver))

def handleIsString(receiver, argument_list=None):
	from interpreting.objects.SelfString import SelfString

	if type(receiver) is not SelfString:
		return argument_list[0].pass_unary_message("value")
	else:
		return receiver

primitive_dict = {
	'_IntAdd:' : handleIntAdd,
	'_AddSlots:' : handleAddSlots,
	'_Assignment:Value:' : handleAssignment,
	'_RunScript' : handleRunScript,
	'_IntNE:' : handleIntNE,
	'_IntLT:' : handleIntLT,
	'_IntLE:' : handleIntLE,
	'_IntEQ:' : handleIntEQ,
	'_IntGT:' : handleIntGT,
	'_IntGE:' : handleIntGE,
	'_Eq:' : handleEq,
	'_IdentityHash' : handleIdentityHash,
	'_IsStringIfFalse:' : handleIsString
}