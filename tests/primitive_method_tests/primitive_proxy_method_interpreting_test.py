import pytest
from interpreting.objects.SelfException import SelfException
from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfString import SelfString

class ThrowawayClass(SelfObject):
	def __init__(self, values):
		self.values = values

	def get_value(self, argument_vector):
		return SelfInteger(self.values[0])

	def get_nth_value(self, argument):
		index = argument.get_value()
		return SelfInteger(self.values[index])

def test_proxy_logic():
	test_obj = ThrowawayClass([0, 1, 2, 3, 4, 5])
	expected_value_one = SelfInteger(0)
	actual_value_one = test_obj.pass_keyword_message("_CallMethodByProxy:Arguments:", [SelfString("get_value"), SelfInteger(0)])

	expected_value_two = SelfInteger(3)
	actual_value_two = test_obj.pass_keyword_message("_CallMethodByProxy:Arguments:", [SelfString("get_nth_value"), SelfInteger(3)])

	assert str(expected_value_one) == str(actual_value_one)
	assert str(expected_value_two) == str(actual_value_two)

def test_proxy_error():
	test_obj = ThrowawayClass([0, 1, 2, 3, 4, 5])

	with pytest.raises(SelfException):
		test_obj.pass_keyword_message("_CallMethodByProxy:Arguments:", [SelfString("non_existant"), SelfInteger(0)])

	with pytest.raises(SelfException):
		test_obj.pass_keyword_message("_CallMethodByProxy:Arguments:", [SelfString("get_zth_value"), SelfInteger(3)])