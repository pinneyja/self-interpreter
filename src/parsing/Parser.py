from parsing.nodes.IntegerNode import *
from parsing.nodes.RegularObjectNode import *
from parsing.nodes.DataSlotNode import *
import ply.lex as lex
import ply.yacc as yacc

class Parser:
	def __init__(self):
		self.lexer = lex.lex(module = self)
		self.parser = yacc.yacc(module = self)

	# Ignored characters

	t_ignore = " \t"

	# Tokens

	tokens = ('INTEGER','LPAREN','RPAREN','PIPE','PERIOD','LARROW','EQUAL',
			'IDENTIFIER')

	t_LPAREN = r'\('
	t_RPAREN = r'\)'
	t_PIPE = r'\|'
	t_PERIOD = r'.'
	t_LARROW = r'<-'
	t_EQUAL = r'='
	t_IDENTIFIER = r'[a-z_][a-zA-Z0-9_]*'

	def t_INTEGER(self, t):
		r'-?\d+'
		t.value = int(t.value)
		return t

	def t_error(self, t):
		print("Illegal character {}".format(t.value[0]))
		t.lexer.skip(1)

	# Productions

	def p_expression_integer(self, p):
		'expression : INTEGER'
		p[0] = IntegerNode(p[1])

	def p_expression_regular_object(self, p):
		'expression : regular-object'
		p[0] = p[1]

	def p_regular_object_empty(self, p):
		'''regular-object : LPAREN RPAREN
						  | LPAREN PIPE PIPE RPAREN'''
		p[0] = RegularObjectNode()

	def p_regular_object_slotted(self, p):
		'regular-object : LPAREN PIPE slot-list PIPE RPAREN'
		p[0] = RegularObjectNode(p[3])

	def p_slot_list(self, p):
		'''slot-list : slot PERIOD slot-list 
					 | slot PERIOD
					 | slot'''
		if(len(p) == 4):
			new_slot_list = p[3]
			new_slot_list.insert(0, p[1])
			p[0] = new_slot_list
		else:
			p[0] = [p[1]]

	def p_slot(self, p):
		'slot : data-slot'
		p[0] = p[1]

	def p_data_slot(self, p):
		'''data-slot : slot-name
					 | slot-name LARROW expression
					 | slot-name EQUAL expression'''
		if(len(p) == 4):
			p[0] = DataSlotNode(p[1], p[2], p[3])
		else:
			p[0] = DataSlotNode(p[1])

	def p_slot_name(self, p):
		'slot-name : IDENTIFIER'
		p[0] = p[1]

	def p_error(self, p):
		print("Syntax error at {}".format(p.value))

	def parse(self, string):
		return self.parser.parse(string)
