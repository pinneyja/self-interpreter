from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty 
from kivy.lang import Builder
from interpreting.objects.gui_objects.SelfGUIObject import SelfGUIObject

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
            # self here refers to the widget i.e FloatLayout
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

	def set_color(self, arg_object):
		r = arg_object.slots['r'].value.get_value()
		g = arg_object.slots['g'].value.get_value()
		b = arg_object.slots['b'].value.get_value()
		a = arg_object.slots['a'].value.get_value()
		self.kivy_widget.set_color(r, g, b, a)
		return self

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

	def set_color(self, r, g, b, a):
		self.background_color = [r, g, b, a]
