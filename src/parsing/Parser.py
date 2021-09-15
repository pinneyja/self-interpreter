from parsing.nodes.IntegerNode import *
import ply.lex as lex
import ply.yacc as yacc

class Parser:
	def __init__(self):
		self.lexer = lex.lex(module = self)
		self.parser = yacc.yacc(module = self)

	# Tokens

	tokens = ('INTEGER',)

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
		# p[0] = ('integer-expression', p[1])
		p[0] = IntegerNode(p[1])

	def p_error(self, p):
		print("Syntax error at {}".format(p.value))

	def parse(self, string):
		return self.parser.parse(string)
