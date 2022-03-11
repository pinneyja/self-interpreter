def handleFloatAdd(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	return handleFloatOperator(receiver, argument_list, lambda x, y: x + y, SelfFloat)

def handleFloatSub(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	return handleFloatOperator(receiver, argument_list, lambda x, y: x - y, SelfFloat)

def handleFloatMul(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	return handleFloatOperator(receiver, argument_list, lambda x, y: x * y, SelfFloat)

def handleFloatDiv(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	return handleFloatOperator(receiver, argument_list, lambda x, y: x / y, SelfFloat)

def handleFloatMod(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	def mod(x, y):
		if (x < 0 and y > 0) or (x > 0 and y < 0):
			return (x % y) - y
		else:
			return x % y
	return handleFloatOperator(receiver, argument_list, mod, SelfFloat)

def handleFloatNE(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleFloatOperator(receiver, argument_list, lambda x, y: x != y, SelfBoolean)

def handleFloatLT(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleFloatOperator(receiver, argument_list, lambda x, y: x < y, SelfBoolean)

def handleFloatLE(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleFloatOperator(receiver, argument_list, lambda x, y: x <= y, SelfBoolean)

def handleFloatEQ(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleFloatOperator(receiver, argument_list, lambda x, y: x == y, SelfBoolean)

def handleFloatGT(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleFloatOperator(receiver, argument_list, lambda x, y: x > y, SelfBoolean)

def handleFloatGE(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleFloatOperator(receiver, argument_list, lambda x, y: x >= y, SelfBoolean)

def handleFloatOperator(receiver, argument, operator, object_type):
	int1 = receiver.get_value()
	int2 = argument.get_value()
	float_result = operator(int1, int2)

	return object_type(float_result)

def handleFloatIfFail(receiver, argument_list, method, primitive_name):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from interpreting.objects.SelfObject import SelfObject
	from Messages import Messages

	argument = argument_list[0]
	if_fail = None
	if len(argument_list) > 1:
		if_fail = argument_list[1]

	if type(receiver) is not SelfFloat or type(argument) is not SelfFloat:
		if if_fail and type(if_fail) is SelfObject:
			return if_fail.pass_keyword_message("value:With:", [SelfString("badTypeError"), SelfString(primitive_name)])
		else:
			raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive_name, receiver, argument))

	return method(receiver, argument)

def handleFloatComparison(receiver, argument_list, operator, primitive_name):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from interpreting.objects.SelfException import SelfException
	from Messages import Messages

	argument = argument_list[0]
	if type(receiver) is not SelfFloat or type(argument) is not SelfFloat:
		raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive_name, receiver, argument))

	float1 = receiver.get_value()
	float2 = argument.get_value()
	boolean_result = operator(float1, float2)

	return SelfBoolean(boolean_result)

def handleFloatCeil(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from Messages import Messages
	from math import ceil

	if type(receiver) is not SelfFloat:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_FloatCeil'))
	return SelfFloat(float(ceil(receiver.value)))

def handleFloatFloor(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from Messages import Messages
	from math import floor

	if type(receiver) is not SelfFloat:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_FloatFloor'))
	return SelfFloat(float(floor(receiver.value)))

def handleFloatRound(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from Messages import Messages

	if type(receiver) is not SelfFloat:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_FloatRound'))
	return SelfFloat(float(round(receiver.value)))

def handleFloatTruncate(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from Messages import Messages
	from math import trunc

	if type(receiver) is not SelfFloat:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_FloatTruncate'))
	return SelfFloat(float(trunc(receiver.value)))

def handleFloatAsInt(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from Messages import Messages

	if type(receiver) is not SelfFloat:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_FloatAsInt'))
	return SelfInteger(round(receiver.value))

def handleNoArgFloatIfFail(receiver, argument_list, no_if_fail_method, primitive_name):
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from interpreting.objects.primitive_objects.SelfString import SelfString

	if type(receiver) is not SelfFloat:
		return argument_list[0].pass_keyword_message("value:With:", [SelfString("badTypeError"), SelfString(primitive_name)])
	return no_if_fail_method(receiver, argument_list)