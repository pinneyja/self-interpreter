import ply.lex as lex
import ply.yacc as yacc
from parsing.nodes.CodeNode import CodeNode
from parsing.nodes.message_nodes.BinaryMessageNode import BinaryMessageNode
from parsing.nodes.message_nodes.KeywordMessageNode import KeywordMessageNode
from parsing.nodes.message_nodes.ResendNode import ResendNode
from parsing.nodes.message_nodes.UnaryMessageNode import UnaryMessageNode
from parsing.nodes.object_nodes.BlockNode import BlockNode
from parsing.nodes.object_nodes.IntegerNode import IntegerNode
from parsing.nodes.object_nodes.FloatNode import FloatNode
from parsing.nodes.object_nodes.StringNode import StringNode
from parsing.nodes.slot_nodes.ArgumentSlotNode import ArgumentSlotNode
from parsing.nodes.slot_nodes.BinarySlotNode import BinarySlotNode
from parsing.nodes.slot_nodes.DataSlotNode import DataSlotNode
from parsing.nodes.slot_nodes.KeywordSlotNode import KeywordSlotNode
from parsing.nodes.slot_nodes.ParentSlotNode import ParentSlotNode
from parsing.utils.AnnotatedList import AnnotatedList
from parsing.utils.ParsingUtils import *

class Parser:
	def __init__(self):
		self.lexer = lex.lex(module = self)
		self.parser = yacc.yacc(module = self)
		self.parse_string = None

	# Ignored characters

	t_ignore = " \t\n"

	# Tokens

	tokens = ('INTEGER','LPAREN','RPAREN','LBRAC','RBRAC','LCBRAC','RCBRAC','PIPE','PERIOD','LARROW','EQUAL',
			'IDENTIFIER', 'PARENT_NAME', 'SMALL_KEYWORD', 'CAP_KEYWORD', 'OPERATOR',
			'COLON', 'STRING', 'CARET', 'DECIMAL', 'FLOAT', 'INTEGER_WITH_BASE', 'RESEND_UNARY',
			'RESEND_BINARY', 'RESEND_KEYWORD')

	t_LPAREN = r'\('
	t_RPAREN = r'\)'
	t_LBRAC = r'\['
	t_RBRAC = r'\]'
	t_LCBRAC = r'\{'
	t_RCBRAC = r'\}'
	t_PIPE = r'\|'
	t_PERIOD = r'\.'
	t_LARROW = r'<\-'
	t_EQUAL = r'='
	t_IDENTIFIER = r'[a-z_][a-zA-Z0-9_]*'
	t_PARENT_NAME = t_IDENTIFIER + r'\*'
	t_SMALL_KEYWORD = r'[a-z_][a-zA-Z0-9_]*:'
	t_CAP_KEYWORD = r'[A-Z][a-zA-Z0-9_]*:'
	t_COLON = r':'
	t_CARET = r'\^'
	normal_operators = r'!@#$%&*+~\/?>,;\\'
	all_operators = normal_operators + t_EQUAL + t_PIPE + t_CARET + t_LARROW
	exclude_larrow = r'(?!<-)'
	t_OPERATOR = (rf'[{all_operators}]{{3,}}|'
		+ rf'{exclude_larrow}[{all_operators}]{{2}}|'
		+ rf'{exclude_larrow}[{normal_operators + t_LARROW}]{{1,2}}')
	t_STRING = r'\'([^\\\']|\\[tbnfrva0\\\'"?]|\\x[0-9a-fA-F]{2}|\\d[0-9]{3}|\\o[0-7]{3})*\''

	def t_RESEND_KEYWORD(self, t):
		r'[a-z_][a-zA-Z0-9_]*[.][a-z_][a-zA-Z0-9_]*[:]'
		tokens = re.split('\\.', t.value)
		t.value = (tokens[0], tokens[1])
		return t

	def t_RESEND_UNARY(self, t):
		r'[a-z_][a-zA-Z0-9_]*[.][a-z_][a-zA-Z0-9_]*'
		tokens = re.split('\\.', t.value)
		t.value = (tokens[0], tokens[1])
		return t

	def t_RESEND_BINARY(self, t):
		r'[a-z_][a-zA-Z0-9_]*[.][!@#$%^&*-+=~/?<>,;|\\]+'
		tokens = re.split('\\.', t.value)
		t.value = (tokens[0], tokens[1])
		return t

	def t_COMMENT(self, t):
		r'\"[^"]*\"'
		pass

	def t_FLOAT(self, t):
		r'-?\d+(.\d+)?[eE][\+-]?\d+'
		return t

	def t_DECIMAL(self, t):
		r'-?\d+[.]\d+'
		return t
	
	def t_INTEGER_WITH_BASE(self, t):
		r'-?\d+[rR][\da-zA-Z]+'
		return t

	def t_INTEGER(self, t):
		r'-?\d+'
		return t

	def t_error(self, t):
		raise SelfParsingError(Messages.SYNTAX_ERROR_AT_TOKEN.value.format(t.value[0]))

	# Precedence Rules

	precedence = (
		('right', 'LOWER'),
		('right', 'HIGHER'),
		('nonassoc', 'LARROW', 'EQUAL'),
		('right', 'SMALL_KEYWORD', 'CAP_KEYWORD'),
		('nonassoc', 'OPERATOR_EQUAL', 'OPERATOR_LARROW'),
		('left', 'OPERATOR'),
		('nonassoc', 'IDENTIFIER')
	)

	# Productions
	def p_code(self, p):
		'''code : expression PERIOD code
				| expression PERIOD
				| expression'''
		if(len(p) == 4):
			p[3].expressions.insert(0, get_first_expression_if_method(p[1]))
			p[0] = p[3]
		else:
			p[0] = CodeNode([get_first_expression_if_method(p[1])])

	def p_code_with_return(self, p):
		'''code : CARET expression PERIOD
				| CARET expression'''
		p[0] = CodeNode([get_first_expression_if_method(p[2])])
		p[0].set_has_caret(True)

	def p_expression(self, p):
		'''expression : constant
					  | unary-message
					  | LPAREN expression RPAREN
					  | binary-message
					  | keyword-message'''
		if (len(p) == 2):
			p[0] = p[1]
		else:
			p[0] = p[2]

	def p_unary_message(self, p):
		'''unary-message : expression IDENTIFIER
						 | IDENTIFIER'''
		if(len(p) == 3):
			p[0] = UnaryMessageNode(p[1], p[2])
		else:
			p[0] = UnaryMessageNode(None, p[1])

	def p_unary_message_resend(self, p):
		'unary-message : RESEND_UNARY'
		p[0] = UnaryMessageNode(ResendNode(p[1][0]), p[1][1])
			
	def p_constant_object(self, p):
		'constant : object'
		p[0] = p[1]

	def p_object(self, p):
		'''object : regular-object
				  | block'''
		p[0] = p[1]

	def p_constant_integer(self, p):
		'constant : INTEGER'
		p[0] = IntegerNode(p[1])
	
	def p_constant_integer_with_base(self, p):
		'constant : INTEGER_WITH_BASE'
		p[0] = IntegerNode(p[1])
	
	def p_constant_decimal(self, p):
		'constant : DECIMAL'
		p[0] = FloatNode(p[1])
	
	def p_constant_float(self, p):
		'constant : FLOAT'
		p[0] = FloatNode(p[1])

	def p_constant_string(self, p):
		'constant : string'
		p[0] = p[1]

	def p_string(self, p):
		'string : STRING'
		s = p[1][1:-1]
		s = convert_d_and_o_escapes_to_x(s)
		s = remove_backslash_from_backslash_question_mark(s)
		p[0] = StringNode(raw_string_to_normal_string(s))

	def p_binary_message(self, p):
		'''binary-message : expression OPERATOR expression
						  | expression LARROW expression %prec OPERATOR_LARROW
						  | expression EQUAL expression %prec OPERATOR_EQUAL
						  | OPERATOR expression
						  | LARROW expression %prec OPERATOR_LARROW
						  | EQUAL expression %prec OPERATOR_EQUAL'''
		if (len(p) == 4):
			p[0] = BinaryMessageNode(p[1], p[2], p[3])
		else:
			p[0] = BinaryMessageNode(None, p[1], p[2])

	def p_binary_message_resend(self, p):
		'binary-message : RESEND_BINARY expression %prec LOWER'
		p[0] = BinaryMessageNode(ResendNode(p[1][0]), p[1][1], p[2])

	def p_keyword_message(self, p):
		'''keyword-message : expression SMALL_KEYWORD expression cap-keyword-expression-list
						   | SMALL_KEYWORD expression cap-keyword-expression-list'''
		if(len(p) == 5):
			p[4][0].insert(0, p[2])
			p[4][1].insert(0, p[3])
			p[0] = KeywordMessageNode(p[1], p[4][0], p[4][1])
		else:
			p[3][0].insert(0, p[1])
			p[3][1].insert(0, p[2])
			p[0] = KeywordMessageNode(None, p[3][0], p[3][1])
	
	def p_keyword_message_resend(self, p):
		'keyword-message : RESEND_KEYWORD expression cap-keyword-expression-list'
		p[3][0].insert(0, p[1][1])
		p[3][1].insert(0, p[2])
		p[0] = KeywordMessageNode(ResendNode(p[1][0]), p[3][0], p[3][1])

	def p_cap_keyword_expression_list(self, p):
		'''cap-keyword-expression-list : CAP_KEYWORD expression cap-keyword-expression-list %prec LOWER
									   | %prec HIGHER'''
		if(len(p) == 4):
			keyword_list = p[3][0]
			value_list = p[3][1]
			keyword_list.insert(0, p[1])
			value_list.insert(0, p[2])
			p[0] = [keyword_list, value_list]
		else:
			p[0] = [[],[]]

	def p_regular_object_empty(self, p):
		'regular-object : LPAREN RPAREN'
		p[0] = RegularObjectNode()

	def p_regular_object_slotted_annotated(self, p):
		'''regular-object : LPAREN PIPE object-annotation slot-list PIPE RPAREN
						  | LPAREN PIPE object-annotation slot-list PIPE code RPAREN'''
		if(len(p) == 7):
			p[0] = RegularObjectNode(p[4], object_annotation=p[3])
		else:
			code_start = p.lexspan(6)[0]
			p_start = p.lexspan(7)[0]
			p[0] = RegularObjectNode(p[4], p[6], object_annotation=p[3], code_string=self.parse_string[code_start:p_start])

	def p_regular_object_slotted(self, p):
		'''regular-object : LPAREN PIPE slot-list PIPE RPAREN
						  | LPAREN PIPE slot-list PIPE code RPAREN'''
		if(len(p) == 6):
			p[0] = RegularObjectNode(p[3])
		else:
			code_start = p.lexspan(5)[0]
			p_start = p.lexspan(6)[0]
			p[0] = RegularObjectNode(p[3], p[5], code_string=self.parse_string[code_start:p_start])

	def p_object_annotation(self, p):
		'''object-annotation : LCBRAC RCBRAC EQUAL string
							 | LCBRAC RCBRAC EQUAL string PERIOD'''
		p[0] = p[4]

	def p_block(self, p):
		'''block : LBRAC PIPE slot-list PIPE RBRAC
				 | LBRAC PIPE slot-list PIPE code RBRAC
				 | LBRAC code RBRAC
				 | LBRAC RBRAC'''
		if len(p) == 7:
			code_start = p.lexspan(5)[0]
			p_start = p.lexspan(6)[0]
			p[0] = BlockNode(p[3], p[5], code_string=self.parse_string[code_start:p_start])
		elif len(p) == 6:
			p[0] = BlockNode(p[3])
		elif len(p) == 4:
			code_start = p.lexspan(2)[0]
			p_start = p.lexspan(3)[0]
			p[0] = BlockNode(code=p[2], code_string=self.parse_string[code_start:p_start])
		else:
			p[0] = BlockNode()

	def p_slot_list_unannotated(self, p):
		'''slot-list : unannotated-slot-list slot-list
					 | '''
		if len(p) == 1:
			p[0] = []
		else:
			p[0] = p[1] + p[2]

	def p_slot_list_annotated(self, p):
		'slot-list : annotated-slot-list slot-list'
		p[2].insert(0, p[1])
		p[0] = p[2]

	def p_annotated_slot_list(self, p):
		'annotated-slot-list : LCBRAC string slot-list RCBRAC'
		p[0] = AnnotatedList(p[2], p[3])

	def p_unannotated_slot_list(self, p):
		'''unannotated-slot-list : slot PERIOD unannotated-slot-list
								 | slot %prec HIGHER
								 | slot PERIOD %prec HIGHER'''
		if(len(p) == 4):
			new_slot_list = p[3]
			new_slot_list.insert(0, p[1])
			p[0] = new_slot_list
		else:
			p[0] = [p[1]]

	def p_slot(self, p):
		'''slot : data-slot
				| binary-slot
				| keyword-slot
				| argument-slot'''
		p[0] = p[1]

	def p_data_slot(self, p):
		'''data-slot : slot-name %prec HIGHER
					 | slot-name LARROW expression
					 | slot-name EQUAL expression'''
		if p[1][-1] == "*":
			if(len(p) == 4):
				p[0] = ParentSlotNode(p[1][:-1], p[2], p[3])
			else:
				p[0] = ParentSlotNode(p[1][:-1])
		else:
			if(len(p) == 4):
				p[0] = DataSlotNode(p[1], p[2], p[3])
			else:
				p[0] = DataSlotNode(p[1])

	def p_binary_slot(self, p):
		'''binary-slot : OPERATOR EQUAL regular-object
					   | LARROW EQUAL regular-object
					   | EQUAL EQUAL regular-object
					   | OPERATOR IDENTIFIER EQUAL regular-object
					   | LARROW IDENTIFIER EQUAL regular-object
					   | EQUAL IDENTIFIER EQUAL regular-object'''
		if(len(p) == 4):
			p[0] = BinarySlotNode(p[1], p[3])
		else:
			p[0] = BinarySlotNode(p[1], p[4], p[2])

	def p_keyword_slot(self, p):
		'''keyword-slot : SMALL_KEYWORD cap-keyword-list EQUAL regular-object
						| SMALL_KEYWORD IDENTIFIER cap-keyword-id-list EQUAL regular-object'''
		if(len(p) == 5):
			p[2].insert(0, p[1])
			p[0] = KeywordSlotNode(p[2], p[4])
		else:
			p[3][0].insert(0, p[1])
			p[3][1].insert(0, p[2])
			p[0] = KeywordSlotNode(p[3][0], p[5], p[3][1])

	def p_cap_keyword_list(self, p):
		'''cap-keyword-list : CAP_KEYWORD cap-keyword-list
							| '''
		if(len(p) == 3):
			keyword_list = p[2]
			keyword_list.insert(0, p[1])
			p[0] = keyword_list
		else:
			p[0] = []

	def p_cap_keyword_id_list(self, p):
		'''cap-keyword-id-list : CAP_KEYWORD IDENTIFIER cap-keyword-id-list
								| '''
		if(len(p) == 4):
			keyword_list = p[3][0]
			arg_list = p[3][1]
			keyword_list.insert(0, p[1])
			arg_list.insert(0, p[2])
			p[0] = [keyword_list, arg_list]
		else:
			p[0] = [[],[]]
			
	def p_argument_slot(self, p):
		'argument-slot : COLON IDENTIFIER'
		p[0] = ArgumentSlotNode(p[2])

	def p_slot_name(self, p):
		'''slot-name : IDENTIFIER
					 | PARENT_NAME
					 '''
		p[0] = p[1]

	def p_error(self, p):
		raise SelfParsingError(Messages.SYNTAX_ERROR_AT_TOKEN.value.format(p.value if p else None))

	def parse(self, string):
		self.parse_string = string
		abstract_syntax_tree = self.parser.parse(string, tracking=True)
		abstract_syntax_tree.verify_syntax()
		self.parse_string = None
		return abstract_syntax_tree