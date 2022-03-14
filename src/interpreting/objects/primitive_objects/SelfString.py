from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.SelfSlot import SelfSlot
from interpreting.objects.primitive_objects.SelfByteVector import SelfByteVector
from interpreting.objects.SelfException import SelfException
from parsing.nodes.CodeNode import CodeNode
from parsing.nodes.message_nodes.KeywordMessageNode import KeywordMessageNode
from parsing.nodes.message_nodes.UnaryMessageNode import UnaryMessageNode

class SelfString(SelfByteVector):
	def __init__(self, value, slots = None, add_traits = True):
		super().__init__(value=value)
		if slots:
			self.slots.update(slots)

		if add_traits:
			from interpreting.objects.primitive_objects.SelfLobby import SelfLobby
			try:
				traits_canonicalString = SelfLobby.get_lobby().slots["traits"].value.pass_unary_message("canonicalString")
				self.parent_slots["parent"] = SelfSlot("parent", traits_canonicalString)
			except SelfException as e:
				pass

	def __str__(self):
		return f"SelfString: (indexable={list(map(str, self.indexable))})"

	def __hash__(self):
		return hash(self.get_value())

	def as_dict(self, visited):
		from interpreting.printingutils.PrinterConfig import CONFIG
		d = {}

		if CONFIG['USE_ALT_STRING']:
			visited.append(self)
		else:
			d = super().as_dict(visited)

		d['type'] = SelfString.__name__
		d['annotation'] = self.get_value()
		d['alt_string'] = True
		return d

	def get_value(self):
		return ''.join(map(lambda x : chr(x.get_value()), self.indexable))