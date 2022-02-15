def handleStringCanonicalize(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from Messages import Messages

	if type(receiver) is SelfString:
		return receiver
	else:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format("_StringCanonicalize"))

def handleStringPrint(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from interpreting.objects.primitive_objects.SelfString import SelfString
	from Messages import Messages

	if type(receiver) is SelfString:
		print(receiver.get_value())
		return receiver
	else:
		raise SelfException(Messages.BAD_TYPE_ERROR.value.format("_StringPrint"))