import re
from interpreting.objects.SelfObject import SelfObject
from interpreting.printingutils.PrinterConfig import add_color, setup_config, CONFIG
import os

class SelfObjectPrinter:
	_instance = None

	def __init__(self):
		if SelfObjectPrinter._instance:
			raise Exception("This class is a singleton!")
		else:
			SelfObjectPrinter._instance = self
			setup_config()

	@staticmethod
	def instance():
		if  SelfObjectPrinter._instance:
			return SelfObjectPrinter._instance
		else:
			return SelfObjectPrinter()

	def get_object_string(self, object:SelfObject):
		object_dict = object.as_dict([])
		return self.construct_object_string(object_dict, 0, 0)

	def construct_object_string(self, object_dict:dict, space_depth:int, object_depth:int):
		if object_depth >= CONFIG['MAX_OBJECT_DEPTH']:
			return add_color('<...>', 'warn')
		
		object_string = add_color(f"{object_dict['type']}: ", 'type') + add_color(self.get_if_non_none('{}', object_dict, 'annotation'), 'annotation')
		if CONFIG['USE_ALT_STRING'] and object_dict['alt_string']:
			return object_string
		
		space_depth += CONFIG['TAB_SIZE']		
		object_slots_dict = object_dict['slots']
		i = 0
		for key in object_slots_dict:
			object_string += '\n' + ' ' * space_depth
			if i >= CONFIG['MAX_LIST_LENGTH']:
				object_string += add_color('...', 'warn')
				break
			object_string += self.construct_slot_string(key, object_slots_dict[key], space_depth, object_depth)
			i += 1

		object_string += '\n' + ' ' * space_depth
		if CONFIG['USE_CODE_STRING'] and object_dict['code_string']:
			code = f"< {object_dict['code_string']} >"
		else:
			code = self.get_if_non_none('{}', object_dict, 'code')
		code = re.sub(r'\s\s+', ' ', code)
		if CONFIG['LIMIT_CODE'] and len(code) > (self.get_terminal_size() - space_depth):
			code = f"{code[:self.get_terminal_size() - space_depth - 4]}..."
		object_string += add_color(code, 'code')

		if not code and len(object_slots_dict) == 0:
			object_string += add_color('<empty>', 'warn')
		return object_string

	def construct_slot_string(self, slot_name:str, slot_dict:dict, space_depth:int, object_depth:int):
		annotations = '-'.join(slot_dict['annotations'])
		if annotations:
			annotations = f"'{annotations}' "
		if CONFIG['LIMIT_SLOT_ANNOTATIONS'] and len(annotations) > (CONFIG['MAX_ANNOTATION_SIZE']):
			annotations = f"{annotations[:CONFIG['MAX_ANNOTATION_SIZE']]}...' "
		if CONFIG['REMOVE_ANNOTATIONS']:
			annotations = '<> '
		slot_name = f"{slot_name}" + ('= ' if slot_dict['is_immutable'] else '. ')
		slot_string = add_color(annotations, 'annotation') + add_color(slot_name, 'slot_name')
		
		slot_object = slot_dict['value']
		if type(slot_object) is dict:
			if len(annotations + slot_name) <= self.get_terminal_size():
				space_depth += len(annotations + slot_name)
			else:
				space_depth += CONFIG['TAB_SIZE']
				slot_string += '\n' + ' ' * space_depth
			slot_string += self.construct_object_string(slot_object, space_depth, object_depth + 1)
		return slot_string

	@staticmethod
	def get_if_non_none(fstring:str, dict:dict, item:str, default:str = ''):
		return fstring.format(dict[item]) if item in dict and dict[item] is not None else default
	
	@staticmethod
	def get_terminal_size():
		return os.get_terminal_size().columns
