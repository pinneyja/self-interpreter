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
	return SelfInteger(len(receiver.indexable))

def handleCopyRangeDstPosSrcSrcPosLength(receiver, argument_list=None):
	dstPos = argument_list[0].value
	src = argument_list[1]
	srcPos = argument_list[2].value
	length = argument_list[3].value

	receiver.indexable[dstPos:dstPos+length] = src.indexable[srcPos:srcPos+length]

	return receiver