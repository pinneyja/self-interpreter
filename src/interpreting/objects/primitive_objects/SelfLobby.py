from ..SelfObject import *
from ..SelfSlot import *

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
			"globals": SelfSlot("globals", SelfObject(annotation="globals", alt_string=True)),
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