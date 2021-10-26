from interpreting.objects.SelfException import *
from Messages import *

def handleIntAdd(receiver, parameter_argument_list):
	from interpreting.objects.SelfInteger import SelfInteger
	argument = parameter_argument_list[0]
	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format("_IntAdd:", receiver, argument))

	return SelfInteger(receiver.get_value() + argument.get_value())

def handleAddSlots(receiver, parameter_argument_list):
	slot_container_object = parameter_argument_list[0]
	receiver.slots.update(slot_container_object.slots)
	receiver.parent_slots.update(slot_container_object.parent_slots)

	return receiver
	
def handleAssignment(receiver, argument_list):
	slot_name = argument_list[0].value
	value = argument_list[1]
	receiver.set_slot(slot_name, value)
	
	return receiver

primitive_dict = {
	'_IntAdd:' : handleIntAdd,
	'_AddSlots:' : handleAddSlots,
	'_Assignment:Value:' : handleAssignment
}