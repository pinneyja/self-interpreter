import traceback
from interpreting.Interpreter import *
from interpreting.printingutils.PrinterConfig import CONFIG
from interpreting.printingutils.SelfObjectPrinter import SelfObjectPrinter
from parsing.Parser import *

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class SelfGUIApp(App):
	def __init__(self):
		super().__init__()

	def build(self):
		self.parser = Parser()
		self.interpreter = Interpreter()
		self.printer = SelfObjectPrinter.instance()
		SelfObjectPrinter.set_color(False)
		bootstrap_failed = False

		try:
			self.interpreter.initializeBootstrap()
		except (SelfException, SelfParsingError) as selfError:
			traceback.print_exc()
			print(selfError)
			print(Messages.BOOTSTRAP_FAILED.value)
			bootstrap_failed = True
		except Exception:
			traceback.print_exc()
			print(Messages.BOOTSTRAP_FAILED.value)
			bootstrap_failed = True

		self.replContainer = BoxLayout(size_hint=(1, 0.25), pos_hint={'x':0, 'y':0.75})

		self.textBox = TextInput(text='')
		self.replContainer.add_widget(self.textBox)

		b = Button(text="Do It", size_hint_x=0.15)
		b.bind(on_press = self.callback)
		self.replContainer.add_widget(b)

		self.output = TextInput(text=Messages.BOOTSTRAP_FAILED.value if bootstrap_failed else '')
		self.replContainer.add_widget(self.output)

		self.layout = self.interpreter.interpret(self.parser.parse("canvas")).kivy_widget
		self.layout.add_widget(self.replContainer)

		return self.layout

	def callback(self, event):
		try:
			obj = self.interpreter.interpret(self.parser.parse(self.textBox.text))
			res = self.printer.get_object_string(obj)
		except Exception as e:
			traceback.print_exc()
			res = str(e)	

		self.output.text = res

def main():
	app = SelfGUIApp()
	app.run()

main()