from interpreting.objects.gui_objects.SelfTextGUIObject import SelfTextGUIObject
from interpreting.objects.primitive_objects.SelfString import SelfString
from kivy.uix.label import Label

class SelfLabel(SelfTextGUIObject):
	def __init__(self):
		super().__init__()
		self.kivy_widget = Label(text="New Label", pos_hint = {'x': 0.0, 'y': 0.0})

	def clone(self):
		clone = super().clone()
		clone.kivy_widget = Label(text=self.kivy_widget.text, size_hint=self.kivy_widget.size_hint, pos_hint=self.kivy_widget.pos_hint)
		return clone

	def __str__(self):
		return f"SelfLabel: text='{self.kivy_widget.text}' size_hint={self.kivy_widget.size_hint} pos_hint={self.kivy_widget.pos_hint}"