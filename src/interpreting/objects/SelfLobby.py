from .SelfObject import *
from .SelfSlot import *
from .SelfInteger import *

class SelfLobby(SelfObject):
	def __init__(self):
		slots = {
			"lobby": SelfSlot("lobby", self),
			"mixins": SelfSlot("mixins", SelfObject()),
			"shell": SelfSlot("shell", SelfObject()),
			"traits": SelfSlot("traits", SelfObject())
			}
		parent_slots = {
			"defaultBehavior": SelfSlot("defaultBehavior", SelfObject()),
			"globals": SelfSlot("globals", SelfObject()),
			}
		super().__init__(slots, parent_slots=parent_slots)

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