# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# Modified from - https://ply.readthedocs.io/en/latest/ply.html
# -----------------------------------------------------------------------------

tokens = ('NUMBER','PLUS','MINUS','TIMES','DIVIDE','LPAREN','RPAREN','NAME','EQUALS')

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

# Ignored characters
t_ignore = " \t" # ignore whitespace

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	print(f"Illegal character {t.value[0]!r}")
	t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
	('left','PLUS','MINUS'),
	('left','TIMES','DIVIDE'),
	('right','UMINUS'),
)

# dictionary of names (for storing variables)
names = { }

def p_statement_assign(p):
	'statement : NAME EQUALS expression'
	p[0] = ('assign-statement', p[1], p[3])

def p_statement_expr(p):
	'statement : expression'
	p[0] = ('expr-statement', p[1])

def p_expression_binop(p):
	'''expression : expression PLUS expression
				  | expression MINUS expression
				  | expression TIMES expression
				  | expression DIVIDE expression'''
	p[0] = ('binop-expression', p[2], p[1], p[3])

def p_expression_uminus(p):
	'expression : MINUS expression %prec UMINUS' # set precedence to be for UMINUS
	p[0] = ('uminus-expression', p[1])

def p_expression_group(p):
	'expression : LPAREN expression RPAREN'
	p[0] = ('group-expression', p[2])

def p_expression_number(p):
	'expression : NUMBER'
	p[0] = ('number-expression', p[1])

def p_expression_name(p):
	'expression : NAME'
	p[0] = ('name-expression', p[1])

def p_error(p):
	print(f"Syntax error at {p.value!r}")

import ply.yacc as yacc
yacc.yacc()

while True:
	try:
		s = input('>>> ')
	except EOFError:
		break
	print(yacc.parse(s))
