from .SelfObject import *
from interpreting.objects.SelfSlot import *
from parsing.nodes.KeywordMessageNode import *
from parsing.nodes.UnaryMessageNode import *

class SelfSmallInt(SelfObject):
	def __init__(self):
		super().__init__()

		arg_slots = OrderedDict()
		arg_slots['arg'] = SelfSlot('arg')
		code = KeywordMessageNode(UnaryMessageNode(None, "self"), ['_IntAdd:'], [UnaryMessageNode(None, 'arg')])
		self.slots['+'] = SelfSlot('+', SelfObject(arg_slots=arg_slots, code=code))