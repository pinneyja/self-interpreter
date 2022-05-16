import traceback
from interpreting.Interpreter import *
from interpreting.printingutils.PrinterConfig import CONFIG
from interpreting.printingutils.SelfObjectPrinter import SelfObjectPrinter
from parsing.Parser import *

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class SelfGUIApp(App):
	def __init__(self):
		super().__init__()

	def build(self):
		self.parser = Parser()
		self.interpreter = Interpreter()
		self.printer = SelfObjectPrinter.instance()
		SelfObjectPrinter.set_color(False)

		try:
			self.interpreter.initializeBootstrap()
		except (SelfException, SelfParsingError) as selfError:
			traceback.print_exc()
			print(selfError)
			print(Messages.BOOTSTRAP_FAILED.value)
		except Exception:
			traceback.print_exc()
			print(Messages.BOOTSTRAP_FAILED.value)

		b = Button(text="Get Lobby", size_hint_x=0.1, size_hint_y=0.1, pos_hint={"x": 0, "y": 0.9})
		b.bind(on_press = self.callback)

		self.layout = self.interpreter.interpret(self.parser.parse("canvas")).kivy_widget
		self.layout.add_widget(b)
		self.interpreter.interpret(self.parser.parse("canvas addOutliner: lobby"))

		return self.layout

	def callback(self, event):
		self.interpreter.interpret(self.parser.parse("canvas addOutliner: lobby"))

def main():
	app = SelfGUIApp()
	app.run()
	print("Running with window size: ", str(Window.size))

main()