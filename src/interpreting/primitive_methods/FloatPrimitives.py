def handleFloatComparison(receiver, argument_list, operator, primitive_name):
	from interpreting.objects.primitive_objects.SelfBoolean import SelfBoolean
	from interpreting.objects.primitive_objects.SelfReal import SelfReal
	from interpreting.objects.SelfException import SelfException
	from Messages import Messages

	argument = argument_list[0]
	if type(receiver) is not SelfReal or type(argument) is not SelfReal:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive_name, receiver, argument))

	float1 = receiver.get_value()
	float2 = argument.get_value()
	boolean_result = operator(float1, float2)

	return SelfBoolean(boolean_result)

def handleFloatEQ(receiver, argument_list):
	return handleFloatComparison(receiver, argument_list, lambda x, y: x == y, "_FloatEQ:")