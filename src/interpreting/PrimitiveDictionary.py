from interpreting.objects.SelfException import SelfException

def handleIntAdd(receiver, parameter_argument_dict):
	from interpreting.objects.SelfInteger import SelfInteger
	argument = parameter_argument_dict['_IntAdd:'].get_value(receiver)
	if type(receiver) is not SelfInteger or type(argument) is not SelfInteger:
		return SelfException(f'Invalid operands for primitive _IntAdd: {receiver}, {argument}')

	return SelfInteger(receiver.get_value() + argument.get_value())

primitive_dict = {
	'_IntAdd:' : handleIntAdd
}