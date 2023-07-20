"""Sorting ints in a file using a bit array."""
from collections.abc import Iterable

# Suppose you must sort and output sorted integer obtained from a file
# containing a subset of unsorted unique integers in the range [a, a + n] (a
# total of n + 1 integers) from a file, and there is no additional data
# attached to the integers. You don't have enough free memory to store the full
# list of integers from the fil in memory and do an in-place sort... Then using
# a bit-array (where each bit represents an integer in the range [a, a + n])
# may be the way to go, since it requires a bit array of only n + 8 // 8 bytes.
# - create a bitarray of (n + 8) // 8 bytes, which is sufficient to hold one
#   bit for each of the n + 1 integers in the range [a, a + n], and initialize
#   all bits to zero.
# - while not all integers were read from file:
#   - read next integer (say a + i) (with 0 <= i <= n) from file,
#   - set bit at position i in the bitarray to 1.
# - for bit position i from 0 to n: if bit at position m in bitarray is set to
#   1, output a + i (if not set to 1, skip it), since a + i was in the file.
#
# 	Considering this is supposed to be a solution for a system low in memory, a
# 	BitArray class is perhaps a luxury, so the implementation uses simple
# 	functions.


def set_bit(bit_array: bytearray, offset: int) -> None:
	"""Set bit in bit_array at 0-based offset. Raises IndexError if offset out
	of bounds."""
	
	bit_array[offset // 8] |= 1 << (offset % 8)


def clear_bit(bit_array: bytearray, offset: int) -> None:
	"""Clear bit in bit_array at 0-based offset. Raises IndexError if offset
	out of bounds."""
	
	bit_array[offset // 8] ^= (1 << (offset % 8))


def _test_bit(bit_array: bytearray, offset: int) -> bool:
	"""Return True if bit in bit_array at offset is set, else False. Raises
	IndexError if offset out of bounds."""
	
	return bit_array[offset // 8] & (1 << (offset % 8)) != 0


def bit_array_get(bit_array: bytearray, start: int, stop: int,
                  bit_status: bool = True) \
	-> Iterable[int]:
	"""Return (sorted) list of offsets in range(start, stop) of all bits in
	bit_array that have bit equal to bit_status."""

	for bit_nr in range(stop - start):
		if _test_bit(bit_array, bit_nr) == bit_status:
			yield start + bit_nr


def _init_bit_array_from_file(start: int, stop: int, filename: str) \
	-> bytearray:
	"""Initialize and return a bytearray with all bits set at offsets that are
	in filename."""
	
	bit_array = bytearray((stop - start + 7) // 8)  # zero-filled by default
	
	with open(filename) as data_file:
		for s in data_file:
			value = int(s)
			if value < start or value >= stop:
				raise ValueError(f"Illegal value {value} "
				                 f"(must be in range({start}, {stop}))")
			set_bit(bit_array, value - start)
	
	return bit_array


def bit_array_get_missing(start: int, stop: int, filename: str) \
	-> Iterable[int]:
	"""Return generator that yields sorted ints that are NOT in filename."""

	bit_array = _init_bit_array_from_file(start, stop, filename)
	yield from bit_array_get(bit_array, start, stop, False)


def bit_array_sort(start: int, stop: int, filename: str) -> Iterable[int]:
	"""Return a generator that yields sorted integers from data_file. The
	integers in the file must all be in range(start, stop)."""
	
	bit_array = _init_bit_array_from_file(start, stop, filename)
	yield from bit_array_get(bit_array, start, stop)
