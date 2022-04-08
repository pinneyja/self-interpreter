from interpreting.objects.gui_objects.SelfTextGUIObject import SelfTextGUIObject
from kivy.uix.textinput import TextInput

class SelfTextInput(SelfTextGUIObject):
	def __init__(self):
		super().__init__()

		self.kivy_widget = TextInput(text="", pos_hint={'x': 0.0, 'y': 0.0}, size_hint = (1.0, 1.0))

	def clone(self):
		clone = super().clone()
		clone.kivy_widget = TextInput(text=self.kivy_widget.text, size_hint=self.kivy_widget.size_hint, pos_hint=self.kivy_widget.pos_hint)
		return clone

	def __str__(self):
		return "SelfTextInput"