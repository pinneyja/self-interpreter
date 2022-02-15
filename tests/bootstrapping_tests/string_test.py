from Messages import Messages
from interpreting.objects.SelfException import SelfException
from interpreting.objects.primitive_objects.SelfByteVector import SelfByteVector
from interpreting.objects.primitive_objects.SelfInteger import SelfInteger
from interpreting.objects.primitive_objects.SelfString import SelfString
from interpreting.objects.primitive_objects.SelfBooleans import SelfBoolean
from interpreting.Interpreter import Interpreter
from parsing.Parser import Parser
import pytest

def test_string_printable_chars(interpreter):
	parser = Parser()

	highest_expected = SelfString('~')
	lowest_expected = SelfString(' ')

	highest_actual = interpreter.interpret(parser.parse("highestPrintableChar"))
	lowest_actual = interpreter.interpret(parser.parse("lowestPrintableChar"))

	assert str(highest_expected) == str(highest_actual)
	assert str(lowest_expected) == str(lowest_actual)

def test_canonical_string(interpreter):
	parser = Parser()

	expected_canonical_string = SelfString('test')
	expected_is_canonical = SelfBoolean(True)
	actual_canonical_string  = interpreter.interpret(parser.parse("'test' canonicalize"))
	actual_byte_vector = interpreter.interpret(parser.parse("'test' _StringCanonicalize"))
	actual_is_canonical = interpreter.interpret(parser.parse("'test' isCanonical"))

	assert str(expected_canonical_string) == str(actual_canonical_string)
	assert str(expected_canonical_string) == str(actual_byte_vector)
	assert str(expected_is_canonical) == str(actual_is_canonical)

def test_bytes_do(interpreter):
	parser = Parser()

	expected_sum = SelfInteger(448)
	actual_sum = interpreter.interpret(parser.parse("lobby _AddSlots: (| sum <- 0 |). 'test' bytesDo: [| :x | lobby sum: sum + x ]. lobby sum"))

	assert str(expected_sum) == str(actual_sum)

def test_string_comparison(interpreter):
	parser = Parser()

	expected_comparison_one = SelfBoolean(True)
	expected_comparison_two = SelfBoolean(False)
	expected_comparison_three = SelfBoolean(False)
	expected_comparison_four = SelfBoolean(False)
	expected_comparison_five = SelfBoolean(True)
	expected_comparison_six = SelfBoolean(True)

	actual_comparison_one = interpreter.interpret(parser.parse("'this is a string' = 'this is a string'"))
	actual_comparison_two = interpreter.interpret(parser.parse("'test one' = 'test two'"))
	actual_comparison_three = interpreter.interpret(parser.parse("'abc' > 'abd'"))
	actual_comparison_four = interpreter.interpret(parser.parse("'abc' < 'abb'"))
	actual_comparison_five = interpreter.interpret(parser.parse("'abcd' > 'abc'"))
	actual_comparison_six = interpreter.interpret(parser.parse("'abcd' < 'abd'"))

	assert str(expected_comparison_one) == str(actual_comparison_one)
	assert str(expected_comparison_two) == str(actual_comparison_two)
	assert str(expected_comparison_three) == str(actual_comparison_three)
	assert str(expected_comparison_four) == str(actual_comparison_four)
	assert str(expected_comparison_five) == str(actual_comparison_five)
	assert str(expected_comparison_six) == str(actual_comparison_six)

def test_prefix_suffix(interpreter):
	parser = Parser()

	expected_comparison_one = SelfBoolean(True)
	expected_comparison_two = SelfBoolean(False)
	expected_comparison_three = SelfBoolean(True)
	expected_comparison_four = SelfBoolean(False)

	actual_comparison_one = interpreter.interpret(parser.parse("'t' isPrefixOf: 'this is a string'"))
	actual_comparison_two = interpreter.interpret(parser.parse("'test one' isPrefixOf: 'test two'"))
	actual_comparison_three = interpreter.interpret(parser.parse("'ing' isSuffixOf: 'this is a string'"))
	actual_comparison_four = interpreter.interpret(parser.parse("'test' isSuffixOf: 'test two'"))

	assert str(expected_comparison_one) == str(actual_comparison_one)
	assert str(expected_comparison_two) == str(actual_comparison_two)
	assert str(expected_comparison_three) == str(actual_comparison_three)
	assert str(expected_comparison_four) == str(actual_comparison_four)

def test_at_put_byte(interpreter):
	parser = Parser()

	with pytest.raises(SelfException, match=Messages.IMMUTABLE_ERROR.value):
		interpreter.interpret(parser.parse("'I am an immutable string!' at: 0 PutByte: 12 IfAbsent: [ unusedCode ]"))

def test_copy(interpreter):
	parser = Parser()

	expected_string = interpreter.interpret(parser.parse("lobby _AddSlots: (| x <- 'test string' |). lobby x"))
	actual_string = interpreter.interpret(parser.parse("lobby x copy"))

	assert expected_string == actual_string

	interpreter.interpret(parser.parse("lobby _AddSlots: (| y <- 'test' copyMutable |). lobby y"))
	interpreter.interpret(parser.parse("lobby _AddSlots: (| z <- lobby y copy |). lobby z"))
	mutated_copy = interpreter.interpret(parser.parse("lobby z at: 0 PutByte: 115 IfAbsent: [ unusedCode ]. lobby z"))
	mutable_original = interpreter.interpret(parser.parse("lobby y"))

	assert str(mutated_copy) != str(mutable_original)

def test_copy_mutable(interpreter):
	parser = Parser()
	
	original_string = interpreter.interpret(parser.parse("lobby _AddSlots: (| x <- 'test' |). lobby x"))
	copied_mutable = interpreter.interpret(parser.parse("lobby _AddSlots: (| y <- lobby x copyMutable |). lobby y"))

	assert original_string != copied_mutable
	with pytest.raises(SelfException, match=Messages.IMMUTABLE_ERROR.value):
		interpreter.interpret(parser.parse("lobby x at: 0 PutByte: 12 IfAbsent: [ unusedCode ]"))

	mutated_mutable = interpreter.interpret(parser.parse("lobby y at: 1 PutByte: 115 IfAbsent: [ unusedCode ]. lobby y"))
	expected_mutation = interpreter.interpret(parser.parse("'tsst' copyMutable"))
	original_string_remade = interpreter.interpret(parser.parse("'test'"))

	assert str(mutated_mutable) == str(expected_mutation)
	assert str(original_string) == str(original_string_remade)

def test_as_byte_vector(interpreter):
	parser = Parser()

	expected_sum = SelfInteger(348)
	actual_sum = interpreter.interpret(parser.parse("lobby _AddSlots: (| sum <- 0 |). (mutableString copySize: 3 FillingWith: 't' asByteVector) bytesDo: [ | :x | lobby sum: lobby sum + x]. lobby sum"))
	byte_vector = interpreter.interpret(parser.parse("'test' copyMutable asByteVector"))

	assert str(expected_sum) == str(actual_sum)
	assert type(byte_vector) == SelfByteVector

def test_copy_size_filling_with(interpreter):
	parser = Parser()

	expected_string_mutable = interpreter.interpret(parser.parse("'testeeee' copyMutable"))
	interpreter.interpret(parser.parse("lobby _AddSlots: (| baseStringImmutable <- 'test'. baseStringMutable <- 'test' copyMutable |)"))
	actual_string_immutable_origin = interpreter.interpret(parser.parse("lobby _AddSlots: (| immutableOrigin <- baseStringImmutable copySize: 8 FillingWith: 101 |). lobby immutableOrigin"))
	actual_string_mutable_origin = interpreter.interpret(parser.parse("lobby _AddSlots: (| mutableOrigin <- baseStringMutable copyMutable copySize: 8 FillingWith: 101 |). lobby mutableOrigin"))

	assert str(expected_string_mutable) == str(actual_string_immutable_origin)
	assert str(expected_string_mutable) == str(actual_string_mutable_origin)

	new_immutable_origin = interpreter.interpret(parser.parse("lobby immutableOrigin at: 0 PutByte: 1. lobby immutableOrigin"))
	new_mutable_origin = interpreter.interpret(parser.parse("lobby mutableOrigin at: 0 PutByte: 2. lobby mutableOrigin"))
	base_string_immutable = interpreter.interpret(parser.parse("lobby baseStringImmutable"))
	base_string_mutable = interpreter.interpret(parser.parse("lobby baseStringImmutable"))
	expected_base_string_immutable = interpreter.interpret(parser.parse("'test'"))
	expected_base_string_mutable = interpreter.interpret(parser.parse("'test' copyMutable"))

	assert str(base_string_immutable) != str(new_immutable_origin)
	assert str(base_string_mutable) != str(new_mutable_origin)
	assert str(base_string_immutable) == str(expected_base_string_immutable)
	assert str(base_string_mutable) == str(expected_base_string_mutable)
	assert str(new_immutable_origin) != str(new_mutable_origin)

def test_string_accessing(interpreter):
	parser = Parser()

	expected_output = interpreter.interpret(parser.parse("'s'"))
	actual_output = interpreter.interpret(parser.parse("'test' at: 2 IfAbsent: [-1]"))

	assert str(expected_output) == str(actual_output)

def test_string_at_put(interpreter):
	parser = Parser()

	expected_output = interpreter.interpret(parser.parse("'tesu'"))
	actual_output = interpreter.interpret(parser.parse("'test' copyMutable at: 3 Put: 'u' IfAbsent: [-1]"))

	assert str(expected_output) == str(actual_output)

def test_string_concatenation(interpreter):
	parser = Parser()

	expected_output = interpreter.interpret(parser.parse("'testing'"))
	actual_output = interpreter.interpret(parser.parse("'test' , 'ing'"))

	assert str(expected_output) == str(actual_output)

def test_string_casing(interpreter):
	parser = Parser()

	expected = interpreter.interpret(parser.parse("'Test test'"))
	actual = interpreter.interpret(parser.parse("'test test' capitalize"))
	assert str(expected) == str(actual)

	expected = interpreter.interpret(parser.parse("'TESTING'"))
	actual = interpreter.interpret(parser.parse("'testing' capitalizeAll"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("'Test' isCapitalized"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("'test' isCapitalized"))
	assert str(expected) == str(actual)

	expected = interpreter.interpret(parser.parse("'testing'"))
	actual = interpreter.interpret(parser.parse("'TEStinG' uncapitalizeAll"))
	assert str(expected) == str(actual)

def test_byte_vector_comparison(interpreter):
	parser = Parser()

	negative_one = interpreter.interpret(parser.parse("-1"))
	zero = interpreter.interpret(parser.parse("0"))
	one = interpreter.interpret(parser.parse("1"))

	expected = negative_one
	actual = interpreter.interpret(parser.parse("'test' _ByteVectorCompare: 'testa'"))
	assert str(expected) == str(actual)

	expected = negative_one
	actual = interpreter.interpret(parser.parse("'azz' _ByteVectorCompare: 'zaz'"))
	assert str(expected) == str(actual)

	expected = negative_one
	actual = interpreter.interpret(parser.parse("'azz' _ByteVectorCompare: 'zza'"))
	assert str(expected) == str(actual)

	expected = negative_one
	actual = interpreter.interpret(parser.parse("'zaz' _ByteVectorCompare: 'zza'"))
	assert str(expected) == str(actual)

	expected = zero
	actual = interpreter.interpret(parser.parse("'zaz' _ByteVectorCompare: 'zaz'"))
	assert str(expected) == str(actual)

	expected = one
	actual = interpreter.interpret(parser.parse("'zaz' _ByteVectorCompare: 'azz'"))
	assert str(expected) == str(actual)

def test_character_methods(interpreter):
	parser = Parser()

	expected = SelfInteger(116)
	actual = interpreter.interpret(parser.parse("'t' asByte"))
	assert str(expected) == str(actual)

	expected = interpreter.interpret(parser.parse("'u'"))
	actual = interpreter.interpret(parser.parse("'' characterFor: 117 IfFail: []"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("'t' isLowerCase"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("'t' isVowel"))
	assert str(expected) == str(actual)

	expected = interpreter.interpret(parser.parse("'c'"))
	actual = interpreter.interpret(parser.parse("'a' succ succ"))
	assert str(expected) == str(actual)

	expected = SelfInteger(116)
	actual = interpreter.interpret(parser.parse("'test' firstByte"))
	assert str(expected) == str(actual)

def test_lines_methods(interpreter):
	parser = Parser()

	expected = interpreter.interpret(parser.parse("'this is'"))
	actual = interpreter.interpret(parser.parse("'this is\na test' firstLine"))
	assert str(expected) == str(actual)

	expected = interpreter.interpret(parser.parse("'a test'"))
	actual = interpreter.interpret(parser.parse("'this is\na test' lastLine"))
	assert str(expected) == str(actual)

def test_matches_pattern(interpreter):
	parser = Parser()

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("'1234aba5678' matchesPattern: '*a?a*'"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("'1234aa5678' matchesPattern: '*a?a*'"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("'1234abba5678' matchesPattern: '*a?a*'"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("'1234aba5678' matchesPattern: 'a?a*'"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(False)
	actual = interpreter.interpret(parser.parse("'test' matchesPattern: 'TEST'"))
	assert str(expected) == str(actual)

	expected = SelfBoolean(True)
	actual = interpreter.interpret(parser.parse("'test' matchesPattern: 'TEST' IgnoreCase: true"))
	assert str(expected) == str(actual)

def test_padding_methods(interpreter):
	parser = Parser()

	expected = interpreter.interpret(parser.parse("'  this\n  is a test'"))
	actual = interpreter.interpret(parser.parse("'this\nis a test' indent: 2"))
	assert str(expected) == str(actual)

	expected = SelfInteger(3)
	actual = interpreter.interpret(parser.parse("'   testing' leadingWhiteSpace"))
	assert str(expected) == str(actual)

	expected = interpreter.interpret(parser.parse("' t    '"))
	actual = interpreter.interpret(parser.parse("('t' padOnLeft: 2) padOnRight: 6"))
	assert str(expected) == str(actual)

def test_as_integer(interpreter):
	parser = Parser()

	expected = SelfInteger(1)
	actual = interpreter.interpret(parser.parse("'1' asInteger"))
	assert str(expected) == str(actual)

	with pytest.raises(Exception):
		actual = interpreter.interpret(parser.parse("'bad' asInteger"))

def test_tokenizing(interpreter):
	parser = Parser()

	expected = SelfInteger(4)
	actual = interpreter.interpret(parser.parse("'this is a test' asWords size"))
	assert str(expected) == str(actual)

	expected = interpreter.interpret(parser.parse("'is'"))
	actual = interpreter.interpret(parser.parse("'this is a test' asWords at: 1"))
	assert str(expected) == str(actual)

	expected = SelfInteger(2)
	actual = interpreter.interpret(parser.parse("('123abc456' breakOnFirstSubstring: 'abc') size"))
	assert str(expected) == str(actual)

	expected = interpreter.interpret(parser.parse("'bc456'"))
	actual = interpreter.interpret(parser.parse("('123abc456' breakOnFirstSubstring: 'abc') at: 1"))
	assert str(expected) == str(actual)

def test_join_using(interpreter):
	parser = Parser()

	expected_str = SelfString('t e s t')
	actual_str = interpreter.interpret(parser.parse("'test' joinUsing: ' '"))

	assert str(expected_str) == str(actual_str)

def test_replace_with(interpreter):
	parser = Parser()

	expected_str = interpreter.interpret(parser.parse("'cccbbbccc' copyMutable"))
	actual_str = interpreter.interpret(parser.parse("'aaabbbaaa' replace: 'a' With: 'c'"))

	assert str(expected_str) == str(actual_str)