from interpreting.primitive_methods.SmallIntPrimitives import *
from interpreting.primitive_methods.FloatPrimitives import *
from interpreting.primitive_methods.ObjectPrimitives import *
from interpreting.primitive_methods.ObjectVectorPrimitives import *
from interpreting.primitive_methods.StringPrimitives import *

primitive_dict = {
	'_IntNE:' : handleIntNE,
	'_IntMod:' : handleIntMod,
	'_IntMul:' : handleIntMul,
	'_IntAdd:' : handleIntAdd,
	'_IntSub:' : handleIntSub,
	'_IntDiv:' : handleIntDiv,
	'_IntLT:' : handleIntLT,
	'_IntLE:' : handleIntLE,
	'_IntEQ:' : handleIntEQ,
	'_IntGT:' : handleIntGT,
	'_IntGE:' : handleIntGE,
	'_IntArithmeticShiftLeft:' : handleIntArithmeticShiftLeft,
	'_IntArithmeticShiftRight:' : handleIntArithmeticShiftRight,
	'_IntLogicalShiftLeft:' : handleIntLogicalShiftLeft,
	'_IntLogicalShiftRight:' : handleIntLogicalShiftRight,
	'_IntOr:' : handleIntOr,
	'_IntAnd:' : handleIntAnd,
	'_IntXor:' : handleIntXor,
	'_IntAsFloat' : handleIntAsFloat,
	'_FloatMul:' : handleFloatMul,
	'_FloatAdd:' : handleFloatAdd,
	'_FloatSub:' : handleFloatSub,
	'_FloatDiv:' : handleFloatDiv,
	'_FloatMod:' : handleFloatMod,
	'_FloatNE:' : handleFloatNE,
	'_FloatLT:' : handleFloatLT,
	'_FloatLE:' : handleFloatLE,
	'_FloatEQ:' : handleFloatEQ,
	'_FloatGT:' : handleFloatGT,
	'_FloatGE:' : handleFloatGE,
	'_FloatCeil' : handleFloatCeil,
	'_FloatFloor' : handleFloatFloor,
	'_FloatRound' : handleFloatRound,
	'_FloatTruncate' : handleFloatTruncate,
	'_FloatAsInt' : handleFloatAsInt,
	'_AddSlots:' : handleAddSlots,
	'_Assignment:Value:' : handleAssignment,
	'_RunScript' : handleRunScript,
	'_RunScriptIfFail:' : handleRunScriptIfFail,
	'_Eq:' : handleEq,
	'_IdentityHash' : handleIdentityHash,
	'_IsStringIfFalse:' : handleIsString,
	'_Clone' : handleClone,
	'_Define:' : handleDefine,
	'_GetSlot:' : handleGetSlot,
	'_CurrentTimeString' : handleCurrentTimeString,
	'_Clone:Filler:' : handleCloneFiller,
	'_At:' : handleAt,
	'_At:Put:' : handleAtPut,
	'_Size' : handleSize,
	'_CopyRangeDstPos:Src:SrcPos:Length:' : handleCopyRangeDstPosSrcSrcPosLength,
	'_StringCanonicalize' : handleStringCanonicalize,
	'_StringPrint' : handleStringPrint,
	'_ByteSize' : handleByteSize,
	'_ByteAt:' : handleByteAt,
	'_ByteAt:IfFail:' : handleByteAtIfFail,
	'_ByteAt:Put:' : handleByteAtPut,
	'_ByteAt:Put:IfFail:' : handleByteAtPutIfFail,
	'_CloneBytes:Filler:' : handleCloneBytesFiller,
	'_CloneBytes:Filler:IfFail:' : handleCloneBytesFillerIfFail,
	'_ByteVectorConcatenate:Prototype:' : handleByteVectorConcatenatePrototype,
	'_ByteVectorConcatenate:Prototype:IfFail:' : handleByteVectorConcatenatePrototypeIfFail,
	'_ByteVectorCompare:' : handleByteVectorCompare,
	'_ByteVectorCompare:IfFail:' : handleByteVectorCompareIfFail,
	'_CopyByteRangeDstPos:Src:SrcPos:Length:' : handleCopyRangeDstPosSrcSrcPosLength,
	'_ThrowError:' : handleThrowError,
	'_Print' : handlePrint
}

class IfFailGenerator():
	def __init__(self, function):
		self.function = function
		self.function_name = ""
		self.if_fail_handler = generic_error_check_fn

	def set_function_name(self, function_name):
		self.function_name = function_name

	def set_if_fail_handler(self, if_fail_handler):
		self.if_fail_handler = if_fail_handler

	def get_function(self):
		return self.function

	def get_if_fail_function(self):
		return error_handler(self.if_fail_handler, self.function, self.function_name)

	def get_function_name(self):
		return self.function_name

def generic_error_check_fn(receiver, argument_list, fn, key_name):
	return fn(receiver, argument_list) # Once refactor is complete, this can be turned into something more meaningful that activates IfFail block

def error_handler(error_check_fn, fn, key_name):
	def error_wrapper(receiver, argument_list):
		return error_check_fn(receiver, argument_list, fn, key_name)

	return error_wrapper

def setup_if_fail_functions():
	int_if_fail_functions = {"_IntNE:", "_IntMod:", "_IntMul:", "_IntAdd:", "_IntSub:", "_IntDiv:", "_IntLT:", "_IntLE:", "_IntEQ:", "_IntGT:", "_IntGE:", "_IntArithmeticShiftLeft:", "_IntArithmeticShiftRight:", "_IntLogicalShiftLeft:", "_IntLogicalShiftRight:", "_IntOr:", "_IntAnd:", "_IntXor:"}
	float_if_fail_functions = {"_FloatMul:", "_FloatAdd:", "_FloatSub:", "_FloatDiv:", "_FloatMod:", "_FloatNE:", "_FloatLT:", "_FloatLE:", "_FloatEQ:", "_FloatGT:", "_FloatGE:"}
	float_if_fail_no_args_functions = {"_FloatCeil", "_FloatFloor", "_FloatRound", "_FloatTruncate", "_FloatAsInt"}

	handler_mappings = [
		[int_if_fail_functions, handleIntIfFail],
		[float_if_fail_functions, handleFloatIfFail], 
		[float_if_fail_no_args_functions, handleNoArgFloatIfFail]]

	for handler_map in handler_mappings:
		for function_name in handler_map[0]:
			fn = primitive_dict[function_name]
			ifFailGenerator = IfFailGenerator(fn)
			ifFailGenerator.set_if_fail_handler(handler_map[1])
			primitive_dict[function_name] = ifFailGenerator

	for function_name in primitive_dict.keys():
		fn = primitive_dict[function_name]
		if type(fn) is not IfFailGenerator:
			primitive_dict[function_name] = IfFailGenerator(fn)

	if_fail_functions = {}
	for key in primitive_dict.keys():
		value = primitive_dict[key]
		if type(value) is list:
			primitive_dict[key] = error_handler(value[0], value[1], key)
		elif type(value) is IfFailGenerator:
			value.set_function_name(key)
			fn_name = value.get_function_name()
			fn = value.get_function()
			fn_handler = value.get_if_fail_function()

			primitive_dict[fn_name] = fn_handler
			if_fail_name = fn_name + "IfFail:"
			if "IfFail:" not in fn_name: # Refactor the IfFail logic to separate out type checking for errors and the actual IfFail invocation to remove this if statement
				if_fail_functions[if_fail_name] = fn_handler

	primitive_dict.update(if_fail_functions)

setup_if_fail_functions()
