from interpreting.objects.SelfObject import SelfObject
from typing import OrderedDict
from interpreting.objects.SelfSlot import SelfSlot
from parsing.nodes.message_nodes.KeywordMessageNode import *
from parsing.nodes.message_nodes.UnaryMessageNode import *

class SelfSmallInt(SelfObject):
	def __init__(self):
		super().__init__()

		arg_slots = OrderedDict()
		arg_slots['arg'] = SelfSlot('arg')
		code = KeywordMessageNode(UnaryMessageNode(None, "self"), ['_IntAdd:'], [UnaryMessageNode(None, 'arg')])
		code_string = "self _IntAdd: arg"
		self.slots['+'] = SelfSlot('+', SelfObject(arg_slots=arg_slots, code=code, code_string=code_string))