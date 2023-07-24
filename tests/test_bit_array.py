"""Tests for function in bit_array.py"""
from random import sample

from bit_array import bit_array_sort, bit_array_get_missing


def write_ints(start: int, stop: int, nr_ints: int, filename: str) -> None:
	"""Write nr_ints UNIQUE integers in range(start, stop) to filename."""
	
	with open(filename, "w") as f:
		for i in sample(range(start, stop, 1), nr_ints):
			f.write(str(i) + "\n")


def test_bit_array_sort() -> None:
	"""Test bit_array_sort function."""

	# The file contains 15.000 integers (one per line) in random order from
	# the range(0, 27000);
	filename = "_15000.ints"
	range_start = 0
	range_stop = 27000
	subset_size = 15000

	b_sorted = list(bit_array_sort(range_start, range_stop, filename))

	with open(filename) as f:
		p_sorted = sorted([int(i) for i in f])

	assert b_sorted == p_sorted
	assert len(b_sorted) == subset_size
	print("\nBitarray sort OK!")
	

def test_bit_array_find_missing() -> None:
	"""Test the bit_array_get_missing function."""
	
	# The file contains 1.000.000 integers (one per line) in random order from
	# the range(0, 2 ** 20) (that is, all can be coded binary with at most 20
	# bits, 1.048.575 = 0b 1111 1111 1111 1111 1111).
	filename = "_20bitints.txt"
	range_start = 0
	range_stop = 2 ** 20
	
	sorted_missing = \
		list(bit_array_get_missing(range_start, range_stop, filename))
	assert len(sorted_missing) == 2 ** 20 - 1_000_000

	set_sorted_missing = set(sorted_missing)
	set_from_file = set([int(i) for i in open(filename)])
	set_all = set(range(2 ** 20))
	assert set_sorted_missing.union(set_from_file) == set_all
	assert set_sorted_missing.intersection(set_from_file) == set()
	print("Bitarray get missing integers OK!")
