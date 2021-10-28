from enum import Enum

class Messages(Enum):
	LOOKUP_ERROR_GENERIC = "Lookup error"
	LOOKUP_ERROR_NO_SLOT = "Lookup error: no matching slot"
	LOOKUP_ERROR_MULTIPLE_SLOTS = "Lookup error: more than one matching slot"
	NOT_A_KEYWORD_SLOT = "Not a keyword slot"
	INVALID_NUMBER_ARG_SLOTS = "Wrong number of argument slots"
	INVALID_UNARY_RECEIVER = "Attempted to pass unary message to invalid receiver."
	INVALID_BINARY_RECEIVER = "Attempted to pass binary message to invalid receiver."
	INVALID_KEYWORD_RECEIVER = "Attempted to pass keyword message to invalid receiver."
	SYNTAX_ERROR_AT_TOKEN = "Syntax error at token: \'{}\'"
	INVALID_ESCAPE_CHARACTER = 'Invalid escape character: \'{}\'.'
	EMPTY_OBJECT_WITH_ARG = "Empty objects cannot have arguments."
	INVALID_PRIMITIVE_OPERANDS = "Invalid operands for primitive {} {}, {}"
	PRIMITIVE_NOT_DEFINED = "Primitive '{}' not defined"
	GENERIC_ERROR = "Unknown error occurred: {}."
	INVALID_BASE = "Integers may only be written using bases from 2 to 36."
	INVALID_DIGIT = "The digit '{}' is not appropriate for the base '{}'."
	MULTIPLE_EXPRESSIONS_IN_SUB_EXPRESSION = "Cannot have multiple expressions inside a sub-expression"