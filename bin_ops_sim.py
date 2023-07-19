"""Module has functions that SIMULATE the bitwise operators:
x & y  == bitwise_and(x, y)
x | y  == bitwise_or(x, y)
x ^ y  == bitwise_xor(x, y)
~ x    == bitwise_not(x)
x << n == shift_left(x, n)
x >> n == shift_right(x, n)

Of course, this is just an exercise, it has no practical use whatsoever. The
fun was mostly in figuring out the way Python stores ints in memory.
"""
import random
from math import copysign
from random import sample

"""A few notes:
Python only lets you do the *arithmetic* shift, NOT te *logical* shift:
- A Left Arithmetic Shift of one position moves each bit to the left by one.
  The vacant least significant bit (LSB) is filled with zero and the most
  significant bit (MSB) is discarded.
- A Left Logical Shift is identical to a Left Arithmetic Shift.
- A Right Logical Shift of one position moves each bit to the right by one.
  The least significant bit is discarded and the vacant MSB is filled with zero.
- A Right Arithmetic Shift of one position moves each bit to the right by one.
  The least significant bit is discarded and the vacant MSB is filled with the
  value of the previous (now shifted one position to the right) MSB.

With a and b integers, and x_i the i-th bit of x (where we start counting with
i = 0 for the lsb at the right) we can simulate bitwise and, or, xor and not:
	(a & b)_i = a_i x b_i
	(a | b)_i = a_i + b_i - (a_i x b_i)
	(a ^ b)_i = (a_i + b_i) % 2
	(~a)_i = 1 - a_i
The arithmetic bitshift operators can be simulated with
	a >> n = a // (2 ** n)
	a << n = a * (2 ** n)
and noticing that 2 ** n = 1 << n also as
	a >> n = a // shift_left(1, n)
	a << n = a * shift_left(1, n),
(We cannot use << and >>, since we are building a simulation of these
operators!)

Python integers are not fixed size and are stored as follows:
- A positive integer i has a magnitude bitlength equal to the required number
  of bits to store the absolute value: 5(10) = 101(2). Immediately befor
  this magnitude is a sign bit (0 for positive integers), so internally 5(10) =
  0101(2).
- A negative intger i is stored as the two's complement of the unsigned
  absolute value of i. For -5(10) this means:
  a) take the binary representation of the absolute value of -5(10) INCLUDING
     the sign bit. 5(10) has binary representation 0101(2)
  b) make one's complement of 0101(2): 1010(2)
  c) add one to 1010(2): 1011(2)
  Then the binary representation of -5(10) is 1011(2).
"""


def _get_bit(i: int, bit_offset: int) -> int:
	"""Return the value (0 or 1) of bit at bit_offset in i."""
	
	return shift_right(i, bit_offset) % 2


def sign(i: int) -> float:
	"""Returns 1.0 if i >= 0, else returns -1.0."""
	
	return copysign(1, i)


def bitwise_xor(op1: int, op2: int) -> int:
	"""Return the result of xor-ing of the operands."""
	
	if op1 == op2 == 0:
		return 0
	nr_bits = max(op1.bit_length(), op2.bit_length())
	sign_value = (sign(op1) != sign(op2)) * shift_left(-1, nr_bits)
	result = ''.join('1' if _get_bit(op1, i) != _get_bit(op2, i) else '0'
	                 for i in range(nr_bits - 1, -1, -1))
	
	return sign_value + int(result, 2)


def bitwise_and(op1: int, op2: int) -> int:
	"""Returns the integer obtained by bitwise and-ing int op1 and op2."""
	
	if op1 == op2 == 0:
		return 0
	nr_bits = max(op1.bit_length(), op2.bit_length())
	sign_value = (op1 < 0 and op2 < 0) * shift_left(-1, nr_bits)
	result = ''.join('1' if _get_bit(op1, i) == _get_bit(op2, i) == 1 else '0'
	                 for i in range(nr_bits - 1, -1, -1))
	
	return sign_value + int(result, 2)


def bitwise_or(op1: int, op2: int) -> int:
	"""Return the result of or-ing of the operands."""
	
	if op1 == op2 == 0:
		return 0
	nr_bits = max(op1.bit_length(), op2.bit_length())
	sign_value = (op1 < 0 or op2 < 0) * shift_left(-1, nr_bits)
	result = ''.join('0' if _get_bit(op1, i) == _get_bit(op2, i) == 0 else '1'
	                 for i in range(nr_bits - 1, -1, -1))
	
	return sign_value + int(result, 2)


def bitwise_not(i: int) -> int:
	"""Return the bitwise not of integer i."""
	
	if i == 0:
		return -1
	
	nr_bits = i.bit_length()
	sign_value = (i > 0) * shift_left(-1, nr_bits)
	result = ''.join(str(1 - _get_bit(i, offset))
	                 for offset in range(nr_bits - 1, -1, -1))
	
	return sign_value + int(result, 2)


def shift_left(i: int, nr_bits: int) -> int:
	"""Return the value of i after ARITHMATIC shift left by nr_bits.
	Notice that arithmetic shift left is the same as logical shift left."""
	
	return int(i * 2 ** nr_bits)


def shift_right(i: int, nr_bits: int) -> int:
	"""Return the value of i after ARITHMATIC shift right by nr_bits."""
	
	return int(i // 2 ** nr_bits)


def _test_all() -> None:
	"""Does all tests..."""
	_test_shifts()
	_test_get_bit()
	_test_bitwise_not()
	_test_bitwise_and()
	_test_bitwise_or()
	_test_bitwise_xor()


def _test_shifts() -> None:
	"""Tests shift_left and shit_rught functions...."""
	
	test_sample = sample(range(-100_000, 100_000), 200)

	for i in test_sample:
		for nr_bits in range(20):
			
			result = shift_left(i, nr_bits)
			expected = i << nr_bits
			assert result == expected, \
				f"shift_left error for {i=}, {nr_bits=}: {result = }, " \
				f"{expected = }"
			
			result = shift_right(i, nr_bits)
			expected = i >> nr_bits
			assert shift_right(i, nr_bits) == i >> nr_bits, \
				f"arithmetic_shift_right error for {i=}, {nr_bits=}: " \
				f"{result = }, {expected = }"
	
	print("shift_tests OK")


def _test_get_bit() -> None:
	"""Does tests for _get_bit function. (This function is also frequently used
	by other funcs, to it is tested in many ways..). """
	
	i_str = ''.join(random.choice(("1", "0")) for _ in range(100))
	i = int(i_str, 2)
	
	for offset, bit in enumerate(reversed(i_str)):
		result = _get_bit(i, offset)
		expected = int(bit)
		assert result == expected, \
			f"get_bit_tests error for {i=}, {offset=}: " \
			f"{result = }, {expected = }"
	
	print("get_bit_tests OK")


def _test_bitwise_and() -> None:
	"""Tests the bitwise and function..."""
	
	r = range(-1000, 1000)
	for i in sample(r, 250) + [-1, 0, 1]:
		for j in sample(r, 250) + [-1, 0, 1]:
			assert bitwise_and(i, j) == (i & j), \
				f"bitwise_and error for {i=}, {j=}:"
	
	print("bitwise_and_tests OK")


def _test_bitwise_or() -> None:
	"""Tests the bitwise and function..."""
	
	r = range(-1000, 1000)
	for i in sample(r, 250) + [-1, 0, 1]:
		for j in sample(r, 250) + [-1, 0, 1]:
			result = bitwise_or(i, j)
			expected = i | j
			assert result == expected, \
				f"bitwise_or error for {i=}, {j=}: {result=}, {expected=}."

	print("bitwise_or_tests OK")


def _test_bitwise_xor() -> None:
	"""Tests the bitwise and function..."""
	
	r = range(-1000, 1000)
	for i in sample(r, 250) + [-1, 0, 1]:
		for j in sample(r, 250) + [-1, 0, 1]:
			result = bitwise_xor(i, j)
			expected = i ^ j
			assert result == expected, \
				f"bitwise_xor error for {i=}, {j=}: {result = }, {expected = }"
	
	print("bitwise_xor_tests OK")


def _test_bitwise_not() -> None:
	"""Tests the bitwise not function..."""
	r = range(-1000, 1000)
	
	for i in sample(r, 250) + [-1, 0, 1]:
		result = bitwise_not(i)
		expected = ~i
		assert result == expected, \
			f"bitwise_not_tests error for {i=}: {result=}, {expected=}"

	print("bitwise_not_tests OK")


_test_all()
