"""Tests for all functions in bin_ops_sim.py."""
from random import sample, choice

from bin_ops_sim import shift_right, shift_left, _get_bit, bitwise_and, \
	bitwise_or, bitwise_xor, bitwise_not, bit_count


binops_range = range(-1000, 1000)
binops_sample = sample(binops_range, 250) + \
                [-98765432198765432198765432198765432100,
                 -1, 0, 1,
                 98765432198765432198765432198765432100]


def test_shifts() -> None:
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


def test_get_bit() -> None:
	"""Does tests for _get_bit function. (This function is also frequently used
	by other funcs, to it is tested in many ways..). """
	
	i_str = ''.join(choice(("1", "0")) for _ in range(100))
	i = int(i_str, 2)
	
	for offset, bit in enumerate(reversed(i_str)):
		result = _get_bit(i, offset)
		expected = int(bit)
		assert result == expected, \
			f"get_bit_tests error for {i=}, {offset=}: " \
			f"{result = }, {expected = }"
	
	print("\nget_bit_tests OK")


def test_bitwise_and() -> None:
	"""Tests the bitwise and function..."""
	global binops_sample
	
	for i in binops_sample:
		for j in binops_sample:
			result = bitwise_and(i, j)
			expected = i & j
			assert result == expected, \
				f"bitwise_and error for {i=}, {j=}: {result = }, {expected = }"
	
	print("bitwise_and_tests OK")


def test_bitwise_or() -> None:
	"""Tests the bitwise and function..."""
	global binops_sample
	
	for i in binops_sample:
		for j in binops_sample:
			result = bitwise_or(i, j)
			expected = i | j
			assert result == expected, \
				f"bitwise_or error for {i=}, {j=}: {result=}, {expected=}."
	
	print("bitwise_or_tests OK")


def test_bitwise_xor() -> None:
	"""Tests the bitwise and function..."""
	global binops_sample
	
	for i in binops_sample:
		for j in binops_sample:
			result = bitwise_xor(i, j)
			expected = i ^ j
			assert result == expected, \
				f"bitwise_xor error for {i=}, {j=}: {result = }, {expected = }"
	
	print("bitwise_xor_tests OK")


def test_bitwise_not() -> None:
	"""Tests the bitwise not function..."""
	global binops_sample
	
	for i in binops_sample:
		result = bitwise_not(i)
		expected = ~i
		assert result == expected, \
			f"bitwise_not_tests error for {i=}: {result=}, {expected=}"
	
	print("bitwise_not_tests OK")


def test_bit_count() -> None:
	s = sample(range(-1_000_000, 1_000_000), 100)
	for i in s:
		assert bit_count(i) == i.bit_count()
