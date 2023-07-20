"""Tests the split_list and split_file functions"""
from random import sample

from find_missing_ints import find_missing_1, find_missing_2


def test_all() -> None:
	_test_find_missing_1()
	_test_find_missing_2()
	

def _test_find_missing_1() -> None:
	filename = "_20bitints.txt"
	missing = find_missing_1(filename, 19)
	assert missing == 595233


def _test_find_missing_2() -> None:
	filename = "_20bitints.txt"
	missing = find_missing_2(filename, 19)
	assert missing == 595233


# Support function, only required to generate input files (should not be done
# without changing the expected value for 'missing' in tests above!!!!)
def write_ints(start: int, stop: int, nr_ints: int, filename: str) -> None:
	"""Write nr_ints UNIQUE integers in range(start, stop) to filename."""

	with open(filename, "w") as f:
		for i in sample(range(start, stop, 1), nr_ints):
			f.write(str(i) + "\n")
