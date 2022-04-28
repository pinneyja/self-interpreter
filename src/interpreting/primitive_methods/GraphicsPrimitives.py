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

def handleSetGUIRepresentation(receiver, argument_list):
	receiver.gui_representation = argument_list[0]
	return receiver

def handleGetGUIRepresentation(receiver, argument_list):
	if receiver.gui_representation:
		return receiver.gui_representation
	else:
		from interpreting.objects.primitive_objects.SelfLobby import SelfLobby
		from interpreting.Interpreter import Interpreter
		from parsing.Parser import Parser

		parser = Parser()
		interpreter = Interpreter(SelfLobby.get_lobby())
		return interpreter.interpret(parser.parse("nil"))

def handleGetName(receiver, argument_list):
	from interpreting.objects.primitive_objects.SelfString import SelfString

	return SelfString(receiver.get_name())