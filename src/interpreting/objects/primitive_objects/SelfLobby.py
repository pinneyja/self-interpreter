from interpreting.objects.SelfObject import SelfObject
from interpreting.objects.SelfSlot import SelfSlot
from interpreting.objects.gui_objects.SelfTextInput import SelfTextInput
from interpreting.objects.gui_objects.SelfButton import SelfButton
from interpreting.objects.gui_objects.SelfLabel import SelfLabel
from interpreting.objects.primitive_objects.SelfByteVector import SelfByteVector
from interpreting.objects.primitive_objects.SelfObjectVector import SelfObjectVector
from interpreting.objects.primitive_objects.SelfString import SelfString
from interpreting.objects.gui_objects.SelfCanvas import SelfCanvas

class SelfLobby(SelfObject):
	lobby = None

	def __init__(self):
		slots = {
			"lobby": SelfSlot("lobby", self),
			"mixins": SelfSlot("mixins", SelfObject(annotation="mixins", alt_string=True)),
			"shell": SelfSlot("shell", SelfObject(annotation="shell", alt_string=True)),
			"traits": SelfSlot("traits", SelfObject(annotation="traits", alt_string=True))
			}
		parent_slots = {
			"defaultBehavior": SelfSlot("defaultBehavior", SelfObject(annotation="defaultBehavior", alt_string=True)),
			"globals": SelfSlot("globals", SelfObject(
				slots = {
					"vector": SelfSlot("vector", SelfObjectVector()),
					"nil": SelfSlot("nil", SelfObject(annotation="nil", alt_string=True)),
					"byteVector": SelfSlot("byteVector", SelfByteVector("")),
					"string": SelfSlot("string", SelfString("", add_traits=False)),
					"mutableString": SelfSlot("mutableString", SelfString("", add_traits=False)),
					"textInput": SelfSlot("textInput", SelfTextInput()),
					"button": SelfSlot("button", SelfButton()),
					"label": SelfSlot("label", SelfLabel()),
					"canvas": SelfSlot("canvas", SelfCanvas(None))},
				annotation="globals", alt_string=True)),
			}
		super().__init__(slots, parent_slots=parent_slots)
		SelfLobby.lobby = self

	def __str__(self):
		output  = "SelfObject:{Slots = ["
		for key in self.slots:
			if key == "lobby":
				output += "lobby,"
			else:
				output += "{},".format(self.slots[key])
		output += "], Argument Slots = ["
		for key in self.arg_slots:
			output += "{},".format(self.arg_slots[key])
		output += "], Parent Slots = ["
		for key in self.parent_slots:
			output += "{},".format(self.parent_slots[key])
		output += "], code={{{}}}".format(self.code)
		return output + "}"

	@staticmethod
	def get_lobby():
		if not SelfLobby.lobby:
			SelfLobby.lobby = SelfLobby()
		return SelfLobby.lobby

	def as_dict(self, visited):
		dict = super().as_dict(visited)
		dict['alt_string'] = True
		return dict