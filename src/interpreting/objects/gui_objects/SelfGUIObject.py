import traceback
from Messages import Messages
from interpreting.objects.SelfException import SelfException
from interpreting.objects.SelfObject import SelfObject

class SelfGUIObject(SelfObject):
	def __init__(self):
		super().__init__()
		self.name = "a gui object"
		if self.__class__ is SelfGUIObject.__class__:
			raise NotImplementedError()

	def add_widget(self, self_widget):
		try:
			self.kivy_widget.add_widget(self_widget.kivy_widget)
		except Exception:
			traceback.print_exc()
			raise SelfException(Messages.ADD_WIDGET_ERROR.value)
		return self

	def remove_widget(self, self_widget):
		try:
			self.kivy_widget.remove_widget(self_widget.kivy_widget)
		except Exception:
			traceback.print_exc()
			raise SelfException(Messages.REMOVE_WIDGET_ERROR.value)
		return self
	
	def close(self, _):	
		try:
			self.kivy_widget.parent.remove_widget(self.kivy_object)
		except Exception:
			traceback.print_exc()
			raise SelfException(Messages.REMOVE_WIDGET_ERROR.value)
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
		from interpreting.objects.gui_objects.SelfScrollableContainer import SelfScrollableContainer

		gui_parent = self.slots['gui_parent'].value
		if gui_parent.__class__ is SelfScrollableContainer:
			self.kivy_widget.width = size_object.slots['width'].value.get_value()*gui_parent.kivy_widget.width
			self.kivy_widget.height = size_object.slots['height'].value.get_value()*gui_parent.kivy_widget.height
		else: 
			self.kivy_widget.size_hint = (size_object.slots['width'].value.get_value(), size_object.slots['height'].value.get_value())
		return self

	def get_size(self, _):
		from interpreting.objects.primitive_objects.SelfFloat import SelfFloat
		from interpreting.objects.SelfSlot import SelfSlot
		from interpreting.objects.gui_objects.SelfScrollableContainer import SelfScrollableContainer
		
		gui_parent = self.slots['gui_parent'].value
		if gui_parent.__class__ is SelfScrollableContainer:
			size = [self.kivy_widget.width/gui_parent.kivy_widget.width,
					self.kivy_widget.height/gui_parent.kivy_widget.height]
		else: 
			size = self.kivy_widget.size_hint
		return SelfObject({
			'width': SelfSlot('width', SelfFloat(float(size[0]))),
			'height': SelfSlot('height', SelfFloat(float(size[1]))),
		})
	
	def set_color(self, arg_object):
		r = arg_object.slots['r'].value.get_value()
		g = arg_object.slots['g'].value.get_value()
		b = arg_object.slots['b'].value.get_value()
		a = arg_object.slots['a'].value.get_value()
		self.kivy_widget.background_color = [r, g, b, a]
		return self
