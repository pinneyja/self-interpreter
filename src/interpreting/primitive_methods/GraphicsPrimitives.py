def handleCallMethodByProxy(receiver, argument_list):
	from interpreting.objects.SelfException import SelfException
	from Messages import Messages

	method = argument_list[0].get_value()
	arguments = argument_list[1]

	try:
		return getattr(receiver, method)(arguments)
	except Exception as e:
		print(e)
		raise SelfException(Messages.PROXY_ERROR.value.format(method))