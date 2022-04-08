from interpreting.objects.gui_objects.SelfGUIObject import SelfGUIObject
from kivy.uix.floatlayout import FloatLayout

class SelfCanvas(SelfGUIObject):
	def __init__(self, kivy_widget = None):
		super().__init__()
		self.kivy_widget = FloatLayout()

	def __str__(self):
		return "SelfCanvas"