from interpreting.objects.primitive_objects.SelfString import SelfString
from interpreting.objects.SelfObject import SelfObject
from kivy.uix.label import Label

class SelfLabel(SelfObject):
	def __init__(self, slots = None):
		super().__init__(slots=slots)

		self.kivy_widget = Label(text="New Label", size_hint=(0.2, 0.1), pos_hint={'x': 0.0, 'y': 0.0})

	def get_text(self, _):
		return SelfString(self.kivy_widget.text)

	def set_text(self, new_text: SelfString):
		self.kivy_widget.text = new_text.get_value()
		return self
	
	def set_position(self, pos_object):
		self.kivy_widget.pos_hint = {'x': pos_object.slots['x'].value.get_value(), 'y': pos_object.slots['y'].value.get_value()}
		return self

	def get_position(self, _):
		from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
		from interpreting.objects.SelfSlot import SelfSlot

		pos = self.kivy_widget.pos_hint
		return SelfObject({
			'x': SelfSlot('x', SelfFloat(pos['x'])),
			'y': SelfSlot('y', SelfFloat(pos['y'])),
		})

	def set_size(self, size_object):
		self.kivy_widget.size_hint = (size_object.slots['width'].value.get_value(), size_object.slots['height'].value.get_value())
		return self

	def get_size(self, _):
		from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
		from interpreting.objects.SelfSlot import SelfSlot

		size = self.kivy_widget.size_hint
		return SelfObject({
			'width': SelfSlot('width', SelfFloat(size[0])),
			'height': SelfSlot('height', SelfFloat(size[1])),
		})

	def clone(self):
		clone = super().clone()
		clone.kivy_widget = Label(text=self.kivy_widget.text, size_hint=self.kivy_widget.size_hint, pos_hint=self.kivy_widget.pos_hint)
		return clone

	def __str__(self):
		return f"SelfLabel: text='{self.kivy_widget.text}' size_hint={self.kivy_widget.size_hint} pos_hint={self.kivy_widget.pos_hint}"