"""Sorting ints in a file using a bit array."""
import time
from collections.abc import Iterable
from random import sample


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


if __name__ == "__main__":

	def write_ints(start: int, stop: int, nr_ints: int, filename: str) -> None:
		"""Write nr_ints UNIQUE integers in range(start, stop) to filename."""
		
		with open(filename, "w") as f:
			for i in sample(range(start, stop, 1), nr_ints):
				f.write(str(i) + "\n")
	
	
	def main() -> None:
		"""Driver code..."""
		
		filename = "_15000.ints"
		range_start = 0
		range_stop = 27000
		subset_size = 15000
		# write_ints(range_start, range_stop, subset_size, filename)
		
		time_start = time.perf_counter_ns()
		b_sorted = list(bit_array_sort(range_start, range_stop, filename))
		time_stop = time.perf_counter_ns()
		
		print(f"Read and converted {len(b_sorted)} integers to sorted list "
		      f"from bit array in "
		      f"{int((time_stop - time_start) * 10 ** -9)} seconds, "
		      f"{int((time_stop - time_start) * 10 ** -6)} milliseconds.")
		
		time_start = time.perf_counter_ns()
		with open(filename) as f:
			p_sorted = sorted([int(i) for i in f])
		time_stop = time.perf_counter_ns()
		print(f"Read and converted {len(p_sorted)} integers to sorted list "
		      f"using Python sorted() in "
		      f"{int((time_stop - time_start) * 10 ** -9)} seconds, "
		      f"{int((time_stop - time_start) * 10 ** -6)} milliseconds.")
		
		assert b_sorted == p_sorted
		assert len(b_sorted) == subset_size
		print("Bitarray sort OK!")
	
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
	
	main()
