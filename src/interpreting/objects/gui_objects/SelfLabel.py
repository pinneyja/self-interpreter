from interpreting.objects.gui_objects.SelfTextGUIObject import SelfTextGUIObject
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_string('''
<SelfLabelWidget>:
	text_size: self.TEXT_AREA[0]*self.width, self.TEXT_AREA[1]*self.height
	valign: 'middle'
	font_size: min(self.MAX_FONT_SIZE, (self.width*self.height)/self.FONT_SCALE_RATE)
	background_color: 0, 0, 0, 0
	canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
''')

class SelfLabel(SelfTextGUIObject):
	def __init__(self):
		super().__init__()
		self.kivy_widget = SelfLabelWidget(text="New Label", pos_hint = {'x': 0.0, 'y': 0.0})

	def clone(self):
		clone = super().clone()
		clone.kivy_widget = SelfLabelWidget(text=self.kivy_widget.text, size_hint=self.kivy_widget.size_hint, pos_hint=self.kivy_widget.pos_hint)
		return clone

	def __str__(self):
		return f"SelfLabel: text='{self.kivy_widget.text}' size_hint={self.kivy_widget.size_hint} pos_hint={self.kivy_widget.pos_hint}"

class SelfLabelWidget(Label):
	MAX_FONT_SIZE = 16
	FONT_SCALE_RATE = 86
	TEXT_AREA = (0.95, 1)