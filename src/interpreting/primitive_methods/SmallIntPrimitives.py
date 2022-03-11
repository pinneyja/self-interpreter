def handleIntNE(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleIntOperator(receiver, argument_list, lambda x, y: x != y, SelfBoolean)

def handleIntLT(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleIntOperator(receiver, argument_list, lambda x, y: x < y, SelfBoolean)

def handleIntLE(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleIntOperator(receiver, argument_list, lambda x, y: x <= y, SelfBoolean)

def handleIntEQ(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleIntOperator(receiver, argument_list, lambda x, y: x == y, SelfBoolean)

def handleIntGT(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleIntOperator(receiver, argument_list, lambda x, y: x > y, SelfBoolean)

def handleIntGE(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
	return handleIntOperator(receiver, argument_list, lambda x, y: x >= y, SelfBoolean)

def handleIntAdd(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: x + y, SelfInteger)

def handleIntSub(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: x - y, SelfInteger)

def handleIntMul(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: x * y, SelfInteger)

def handleIntDiv(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	import math
	def div(x, y):
		result = x / y
		if result > 0:
			return math.floor(result)
		else:
			return math.ceil(result)
	return handleIntOperator(receiver, argument_list, div, SelfInteger)

def handleIntMod(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	def mod(x, y):
		if (x < 0 and y > 0) or (x > 0 and y < 0):
			return (x % y) - y
		else:
			return x % y
	return handleIntOperator(receiver, argument_list, mod, SelfInteger)

sign_bit_mask = 1 << 29
thirty_ones = (1 << 30) - 1
def pythonIntTo30BitSigned(x):
	has_sign_bit = bool(x & sign_bit_mask)
	res = x & thirty_ones
	if has_sign_bit:
		res += ~ thirty_ones
	return res

def handleIntArithmeticShiftLeft(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: pythonIntTo30BitSigned(x << (y & 0b11111)), SelfInteger)

def handleIntArithmeticShiftRight(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: x >> (y & 0b11111), SelfInteger)

def handleIntLogicalShiftLeft(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: pythonIntTo30BitSigned(x << (y & 0b11111)), SelfInteger)

def handleIntLogicalShiftRight(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	def logicalShiftRight(x, y):
		return (x & thirty_ones) >> (y & 0b11111)

	return handleIntOperator(receiver, argument_list, logicalShiftRight, SelfInteger)

def handleIntOr(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: x | y, SelfInteger)

def handleIntAnd(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: x & y, SelfInteger)

def handleIntXor(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	return handleIntOperator(receiver, argument_list, lambda x, y: x ^ y, SelfInteger)

def handleIntOperator(receiver, argument, operator, object_type):
	int1 = receiver.get_value()
	int2 = argument.get_value()
	integer_result = operator(int1, int2)

	return object_type(integer_result)

def handleIntIfFail(receiver, argument_list, method, primitive_name):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from interpreting.objects.SelfObject import SelfObject
	from Messages import Messages

	argument = argument_list[0]
	if_fail = None
	if len(argument_list) > 1:
		if_fail = argument_list[1]

	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		if if_fail and type(if_fail) is SelfObject:
			return if_fail.pass_keyword_message("value:With:", [SelfString("badTypeError"), SelfString(primitive_name)])
		else:
			raise SelfException(Messages.INVALID_PRIMITIVE_OPERANDS.value.format(primitive_name, receiver, argument))

	return method(receiver, argument)

def handleIntAsFloat(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
	from Messages import Messages

	if type(receiver) is not SelfInteger:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format('_IntAsFloat'))
	return SelfFloat(float(receiver.value))