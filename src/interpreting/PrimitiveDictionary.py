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

def handleComparison(receiver, argument_list, operator, primitive_name):
	from interpreting.objects.SelfBoolean import SelfBoolean
	from interpreting.objects.SelfInteger import SelfInteger
	argument = argument_list[0]
	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive_name, receiver, argument))

	int1 = receiver.get_value()
	int2 = argument.get_value()
	boolean_result = operator(int1, int2)

	return SelfBoolean(boolean_result)

def handleIntNE(receiver, argument_list):
	return handleComparison(receiver, argument_list, lambda x, y: x != y, "_IntNE:")

def handleIntLT(receiver, argument_list):
	return handleComparison(receiver, argument_list, lambda x, y: x < y, "_IntLT:")

def handleIntLE(receiver, argument_list):
	return handleComparison(receiver, argument_list, lambda x, y: x <= y, "_IntLE:")

def handleIntEQ(receiver, argument_list):
	return handleComparison(receiver, argument_list, lambda x, y: x == y, "_IntEQ:")

def handleIntGT(receiver, argument_list):
	return handleComparison(receiver, argument_list, lambda x, y: x > y, "_IntGT:")

def handleIntGE(receiver, argument_list):
	return handleComparison(receiver, argument_list, lambda x, y: x >= y, "_IntGE:")

primitive_dict = {
	'_IntAdd:' : handleIntAdd,
	'_AddSlots:' : handleAddSlots,
	'_Assignment:Value:' : handleAssignment,
	'_IntNE:' : handleIntNE,
	'_IntLT:' : handleIntLT,
	'_IntLE:' : handleIntLE,
	'_IntEQ:' : handleIntEQ,
	'_IntGT:' : handleIntGT,
	'_IntGE:' : handleIntGE
}