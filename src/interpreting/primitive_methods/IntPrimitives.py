def handleIntAdd(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from Messages import Messages
	
	argument = argument_list[0]
	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format("_IntAdd:", receiver, argument))

	return SelfInteger(receiver.get_value() + argument.get_value())

def handleIntComparison(receiver, argument_list, operator, primitive_name):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from Messages import Messages
	from interpreting.objects.primitive_objects.SelfBoolean import SelfBoolean
	
	argument = argument_list[0]
	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive_name, receiver, argument))

	int1 = receiver.get_value()
	int2 = argument.get_value()
	boolean_result = operator(int1, int2)

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