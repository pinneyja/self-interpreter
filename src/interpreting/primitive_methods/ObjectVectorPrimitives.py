def handleCloneFiller(receiver, argument_list):
	size = argument_list[0].value
	filler = argument_list[1]

	result = receiver.clone()
	result.indexable = receiver.indexable[:size]
	if len(result.indexable) < size:
		result.indexable += [filler for i in range(size-len(result.indexable))]

	return result

def handleAt(receiver, argument_list):
	index = argument_list[0].value

	return receiver.indexable[index]

def handleAtPut(receiver, argument_list):
	index = argument_list[0].value
	new = argument_list[1]

	receiver.indexable[index] = new
	return receiver

def handleSize(receiver, argument_list=None):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from Messages import Messages
	from interpreting.objects.SelfException import SelfException
	if (hasattr(receiver, "indexable")):
		return SelfInteger(len(receiver.indexable))
	else:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format("_Size"))

def handleNoArgIndexableIfFail(receiver, argument_list, no_if_fail_method, primitive_name):
	from interpreting.objects.primitive_objects.SelfString import SelfString

	if not hasattr(receiver, "indexable"):
		return argument_list[0].pass_keyword_message("value:With:", [SelfString("badTypeError"), SelfString(primitive_name)])
	return no_if_fail_method(receiver, argument_list)

def handleCopyRangeDstPosSrcSrcPosLength(receiver, argument_list=None):
	dstPos = argument_list[0].value
	src = argument_list[1]
	srcPos = argument_list[2].value
	length = argument_list[3].value

	receiver.indexable[dstPos:dstPos+length] = src.indexable[srcPos:srcPos+length]

	return receiver

def handleByteSize(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfByteVector import SelfByteVector
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	from Messages import Messages

	if type(receiver) is SelfByteVector or type(receiver) is SelfString:
		return SelfInteger(len(receiver.indexable))
	else:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format("_ByteSize"))

def handleByteAt(receiver, argument_list):
	return receiver.indexable[argument_list[0].value]

def handleByteAtIfFail(receiver, argument_list):
	return handleIfFail(handleByteAt, receiver, argument_list, 1)

def handleByteAtPut(receiver, argument_list):
	index = argument_list[0].value
	new = argument_list[1]

	receiver.indexable[index] = new
	return receiver

def handleByteAtPutIfFail(receiver, argument_list):
	return handleIfFail(handleByteAtPut, receiver, argument_list, 2)

def handleCloneBytesFiller(receiver, argument_list):
	return handleCloneFiller(receiver, argument_list)

def handleCloneBytesFillerIfFail(receiver, argument_list):
	return handleIfFail(handleCloneBytesFiller, receiver, argument_list, 2)

def handleByteVectorConcatenatePrototype(receiver, argument_list):
	add_to_end = argument_list[0].indexable
	prototype = argument_list[1]

	result = prototype.clone()
	result.indexable = receiver.indexable + add_to_end
	return result

def handleByteVectorConcatenatePrototypeIfFail(receiver, argument_list):
	return handleIfFail(handleByteVectorConcatenatePrototype, receiver, argument_list, 2)

def handleByteVectorCompare(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
	
	other = argument_list[0]
	us = list(map(lambda x: x.value, receiver.indexable))
	them = list(map(lambda x: x.value, other.indexable))

	if us > them:
		return SelfInteger(1)
	elif us < them:
		return SelfInteger(-1)
	else:
		return SelfInteger(0)

def handleByteVectorCompareIfFail(receiver, argument_list):
	return handleIfFail(handleByteVectorCompare, receiver, argument_list, 1)

def handleIfFail(method, receiver, argument_list, index):
	from interpreting.objects.SelfException import SelfException

	try:
		return method(receiver, argument_list)
	except SelfException:
		return argument_list[index].pass_unary_message("value")