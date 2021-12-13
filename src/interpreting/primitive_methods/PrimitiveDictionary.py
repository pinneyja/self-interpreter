from interpreting.primitive_methods.IntPrimitives import *
from interpreting.primitive_methods.FloatPrimitives import *
from interpreting.primitive_methods.ObjectPrimitives import *

primitive_dict = {
	'_IntAdd:' : handleIntAdd,
	'_AddSlots:' : handleAddSlots,
	'_Assignment:Value:' : handleAssignment,
	'_RunScript' : handleRunScript,
	'_IntNE:' : handleIntNE,
	'_IntLT:' : handleIntLT,
	'_IntLE:' : handleIntLE,
	'_IntEQ:' : handleIntEQ,
	'_IntGT:' : handleIntGT,
	'_IntGE:' : handleIntGE,
	'_Eq:' : handleEq,
	'_IdentityHash' : handleIdentityHash,
	'_IsStringIfFalse:' : handleIsString,
	'_Clone' : handleClone,
	'_Define:' : handleDefine
}