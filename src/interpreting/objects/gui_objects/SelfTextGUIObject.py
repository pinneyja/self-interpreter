from interpreting.objects.gui_objects.SelfGUIObject import SelfGUIObject
from interpreting.objects.primitive_objects.SelfString import SelfString

class SelfTextGUIObject(SelfGUIObject):
	def __init__(self):
		super().__init__()
		if self.__class__ is SelfTextGUIObject.__class__:
			raise NotImplementedError()
	
	def get_text(self, _):
		return SelfString(self.kivy_widget.text)

	def set_text(self, new_text: SelfString):
		self.kivy_widget.text = new_text.get_value()
		return self