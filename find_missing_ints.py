"""Finding one (or all) missing ints in a list of bounded integers."""
import operator
from os import remove
from random import choice
from string import ascii_lowercase


def _test_int_bit(i: int, offset: int) -> bool:
	return (i & (1 << offset)) != 0


def random_str(length: int) -> str:
	"""Return a random string of specified length, existing of lowercase ascii
	chars."""
	
	letters = ascii_lowercase
	return '__' + ''.join(choice(letters) for _ in range(length))


def find_missing_1(filename: str, max_bit_offset: int) -> int:
	"""Return a missing number WITHOUT reading ints from input in a list or
	using a bitmap. It recursively reads files, splits them into two files,
	then reads and splits the smallest, until one file has NO items. Then
	a missing int can be determined..."""
	
	def _split_file(input_name: str, _bit_nr: int,
	                delete_input_tape: bool = False) -> int:
		"""Recursive function. Returns when one of the two files is empty and
		an int is therefore found that was NOT in the original file (that is
		the input_name on first call)."""
		
		# Adding "1" and "2" guarantees the names are different, since
		# random_str only uses lowercase ascii, no numerals.
		output_names = [random_str(8) + "1.txt", random_str(8) + "2.txt"]
		counts = [0, 0]
	
		with open(input_name) as input_tape:
			output_tapes = [open(output_names[0], "w"),
			                open(output_names[1], "w")]
			for int_str in input_tape:
				# value = int(int_str)
				bit_value = _test_int_bit(int(int_str), _bit_nr)
				output_tapes[bit_value].write(int_str)
				counts[bit_value] += 1
			output_tapes[0].close()
			output_tapes[1].close()
	
		# the bit operator is used to construct the missing int (if applicable
		# yet). If the original 0-bit variant is empty, we must xor a value from
		# the 1-bit variant to get a missing integer
		# Say after _bit_nr = n we have that there are no ints with bit at
		# offset n equal to 0. Then from any number i in the other file (with
		# bit at offset n equal to 1) a missing int can be constructed by
		# setting its bit at offset n to 0, since then (say n = 4):
		# operator.xor(....xxxx1xxxx, ...000010000) = ...xxxx0xxxx will be
		# a missing integer).
		# If there are no ints with bit at offset n equal to 1, then with x
		# operator.or(....xxxx0xxxx, ...000010000) = ....xxxx1xxxx will be
		# a missing integer)

		bit_operator = operator.xor
		if counts[0] > counts[1]:
			# Make sure that the smallest file (and connected data) is at
			# offset 0 (makes the remainder of the code easier to read).
			output_names[0], output_names[1] = output_names[1], output_names[0]
			counts[0], counts[1] = counts[1], counts[0]
			bit_operator = operator.or_
	
		if counts[0] == 0:
			with open(output_names[1]) as f:
				int_str = f.readline()
			missing = bit_operator(int(int_str), 1 << _bit_nr)
			if delete_input_tape:
				remove(input_name)
			remove(output_names[0])
			remove(output_names[1])
			return int(missing)
		else:
			if delete_input_tape:
				remove(input_name)
			remove(output_names[1])
			return _split_file(output_names[0], _bit_nr - 1, True)
	
	return _split_file(filename, max_bit_offset)


def find_missing_2(filename: str, max_bit_offset: int) -> int:
	"""Same as find_missing_1, but this version uses lists to store all
	integers, so it only reads one file. It would be more efficient to use
	a bitarray, but this is an exercise without any practical use..."""
	
	def _find_missing_2(integers: list[int], _bit_nr: int) -> int:
		output_tapes: list[list[int]] = [[], []]
		for i in integers:
			output_tapes[_test_int_bit(i, _bit_nr)].append(i)
		
		bit_operator = operator.xor
		if len(output_tapes[0]) > len(output_tapes[1]):
			output_tapes[0], output_tapes[1] = output_tapes[1], output_tapes[0]
			bit_operator = operator.or_
		
		if len(output_tapes[0]) == 0:
			return int(bit_operator(output_tapes[1][0], 1 << _bit_nr))
		else:
			return _find_missing_2(output_tapes[0], _bit_nr - 1)

	with open(filename) as f:
		list_of_ints = [int(i) for i in f]

	return _find_missing_2(list_of_ints, max_bit_offset)
