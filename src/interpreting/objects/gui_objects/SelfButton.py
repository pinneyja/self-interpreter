from kivy.uix.button import Button
from interpreting.objects.gui_objects.SelfTextGUIObject import SelfTextGUIObject

class SelfButton(SelfTextGUIObject):
	def __init__(self):
		super().__init__()

		self.kivy_widget = Button(text="New Button", pos_hint = {'x': 0.0, 'y': 0.0})
		self.kivy_widget.bind(on_press=self.on_press_callback, on_release=self.on_release_callback)

	def on_press_callback(self, event):
		try:
			self.pass_unary_message("onPress")
		except Exception as e:
			print(e)

	def on_release_callback(self, event):
		try:
			self.pass_unary_message("onRelease")
		except Exception as e:
			print(e)
			
	def clone(self):
		clone = super().clone()
		clone.kivy_widget = Button(text=self.kivy_widget.text, size_hint=self.kivy_widget.size_hint, pos_hint=self.kivy_widget.pos_hint)
		clone.kivy_widget.bind(on_press=clone.on_press_callback, on_release=clone.on_release_callback)
		return clone

	def __str__(self):
		return "SelfButton"
