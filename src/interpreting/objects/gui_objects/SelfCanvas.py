from interpreting.objects.SelfObject import SelfObject
from Messages import Messages

class SelfCanvas(SelfObject):
	def __init__(self, kivy_widget, slots = None):
		super().__init__(slots=slots)
		self.kivy_widget = kivy_widget

	def __str__(self):
		return "SelfCanvas"

	def add_widget(self, self_widget):
		try:
			self.kivy_widget.add_widget(self_widget.kivy_widget)
		except Exception:
			raise SelfException(Messages.ADD_WIDGET_ERROR.value)

	def remove_widget(self, self_widget):
		try:
			self.kivy_widget.remove_widget(self_widget.kivy_widget)
		except Exception:
			raise SelfException(Messages.REMOVE_WIDGET_ERROR.value)