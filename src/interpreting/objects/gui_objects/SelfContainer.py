from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.lang import Builder
from interpreting.objects.gui_objects.SelfGUIObject import SelfGUIObject
from interpreting.objects.SelfObject import SelfObject

Builder.load_string('''
<SelfObjectWindow>
	orientation: 'vertical'
	drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
	canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
''')

class SelfContainer(SelfGUIObject):
	def __init__(self):
		super().__init__()
		self.kivy_widget = SelfObjectWindow()
	
	def get_orientation(self, _):
		from interpreting.objects.primitive_objects.SelfString import SelfString
		return SelfString(self.kivy_widget.orientation)

	def set_orientation(self, arg_string):
		self.kivy_widget.orientation = arg_string.get_value()
		return self

	def set_position(self, pos_object):
		if self.kivy_widget.get_parent_window():
			parent_width = self.kivy_widget.get_parent_window().width
			parent_height = self.kivy_widget.get_parent_window().height
		else:
			parent_width = 1
			parent_height = 1
		self.kivy_widget.pos = [pos_object.slots['x'].value.get_value() * parent_width, pos_object.slots['y'].value.get_value() * parent_height]
		return self

	def get_position(self, _):
		from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
		from interpreting.objects.SelfSlot import SelfSlot

		if self.kivy_widget.get_parent_window():
			parent_width = self.kivy_widget.get_parent_window().width
			parent_height = self.kivy_widget.get_parent_window().height
		else:
			parent_width = 1
			parent_height = 1
		pos = self.kivy_widget.pos
		return SelfObject({
			'x': SelfSlot('x', SelfFloat(pos[0]/parent_width)),
			'y': SelfSlot('y', SelfFloat(pos[1]/parent_height)),
		})

	def clone(self):
		clone = super().clone()
		clone.kivy_widget = SelfObjectWindow(
								size_hint=self.kivy_widget.size_hint, 
								pos_hint=self.kivy_widget.pos_hint, 
								orientation=self.kivy_widget.orientation,
								background_color=self.kivy_widget.background_color)
		return clone

class SelfObjectWindow(DragBehavior, BoxLayout):
	background_color = ListProperty()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.background_color = [0.1, 0.4, 0.4, 1]
		self.size_hint = (1.0, 1.0)