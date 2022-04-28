import traceback
from Messages import Messages
from interpreting.objects.SelfException import SelfException
from interpreting.objects.gui_objects.SelfGUIObject import SelfGUIObject
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

kv_vert = '''
<SelfGridLayout>:
	cols: 1	
	rows: None
	height: self.minimum_height
	size_hint_y: None
	size_hint_x: 1

<ScrollView>:
	size_hint_x: 1
	do_scroll_x: False
	scroll_timeout: 2500
	effect_cls: 'ScrollEffect'
	scroll_wheel_distance: (root.height / 600) * 80
	background_color: 0, 0, 0, 0
	canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size

'''

kv_hor = '''
<SelfGridLayout>:
	rows: 1	
	cols: None
	width: self.minimum_width
	size_hint_x: None
	size_hint_y: 1

<ScrollView>:
	size_hint_y: 1
	do_scroll_y: False
	scroll_timeout: 2500
	effect_cls: 'ScrollEffect'
	scroll_wheel_distance: (root.width / 600) * 80
	background_color: 0, 0, 0, 0
	canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size

'''

class SelfScrollableContainer(SelfGUIObject):
	def __init__(self):
		super().__init__()
		self.vertical_orientation = True
		self.setup_object()

	def setup_object(self):
		Builder.load_string(kv_vert if self.vertical_orientation else kv_hor)
		self.kivy_widget = SelfScrollView()
		self.layout = SelfGridLayout()
		self.kivy_widget.add_widget(self.layout)

	def add_widget(self, self_widget):
		try:
			if self.vertical_orientation:
				size_y = self_widget.kivy_widget.size_hint_y
				self_widget.kivy_widget.size_hint_y = None
				self_widget.kivy_widget.height = size_y*self.kivy_widget.height
			else:
				size_x = self_widget.kivy_widget.size_hint_x
				self_widget.kivy_widget.size_hint_x = None
				self_widget.kivy_widget.width = size_x*self.kivy_widget.width
			self.layout.add_widget(self_widget.kivy_widget)
		except Exception:
			traceback.print_exc()
			raise SelfException(Messages.ADD_WIDGET_ERROR.value)
		return self
	
	def get_orientation(self, _):
		from interpreting.objects.primitive_objects.SelfString import SelfString
		return SelfString('vertical' if self.vertical_orientation else 'horizontal')

	def set_orientation_clone(self, arg_string):
		self.vertical_orientation = arg_string.get_value() == 'vertical'
		self.setup_object()
		return self

	def remove_widget(self, self_widget):
		try:
			self.layout.remove_widget(self_widget.kivy_widget)
		except Exception:
			traceback.print_exc()
			raise SelfException(Messages.REMOVE_WIDGET_ERROR.value)
		return self

	def clone(self):
		clone = super().clone()
		clone.setup_object()
		clone.kivy_widget.size_hint = self.kivy_widget.size_hint	
		clone.kivy_widget.size = self.kivy_widget.size
		clone.kivy_widget.pos_hint = self.kivy_widget.pos_hint
		return clone

class SelfGridLayout(GridLayout):
	pass

class SelfScrollView(ScrollView):
	pass