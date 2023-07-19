"""Finding one (or all) missing ints in a list of bounded integers."""
import operator
from os import remove
from random import sample, choice
from string import ascii_lowercase


def _test_int_bit(i: int, offset: int) -> bool:
	return (i & (1 << offset)) != 0


def random_str(length: int) -> str:
	"""Return a random string of specified length, existing of lowercase ascii
	chars."""
	
	letters = ascii_lowercase
	return '__' + ''.join(choice(letters) for _ in range(length))


def split_tape(i_tape: str, bit_nr: int) -> int:
	"""Return a missing number WITHOUT reading ints from input in a list and
	without using a bitmap. Is splits the tape in two new tapes..."""
	def _split_tape(input_name: str, _bit_nr: int,
	                delete_input_tape: bool = False) -> int:
		output_names = [random_str(8) + ".txt", random_str(8) + ".txt"]
		counts = [0, 0]
	
		with open(input_name) as input_tape:
			output_tapes = [open(output_names[0], "w"),
			                open(output_names[1], "w")]
			for int_str in input_tape:
				value = int(int_str)
				bit_value = _test_int_bit(value, _bit_nr)
				output_tapes[bit_value].write(int_str)
				counts[bit_value] += 1
			output_tapes[0].close()
			output_tapes[1].close()
	
		bit_operator = operator.xor
		if counts[0] > counts[1]:
			output_names[0], output_names[1] = output_names[1], output_names[0]
			counts[0], counts[1] = counts[1], counts[0]
			bit_operator = operator.or_
	
		if counts[0] == 0:
			with open(output_names[1]) as f:
				int_str = f.readline()
			missing = bit_operator(int(int_str), 1 << _bit_nr)
			remove(input_name)
			remove(output_names[0])
			remove(output_names[1])
			return int(missing)
		else:
			if delete_input_tape:
				remove(input_name)
			remove(output_names[1])
			return _split_tape(output_names[0], _bit_nr - 1, True)
	
	return _split_tape(i_tape, bit_nr)


def split_list(input_tape: list[int], bit_nr: int) -> int:
	"""Reads input_tape and splits it in two new tapes:
	 - the first output tape contains all numbers from the input tape that have
	   bit at position bitnr equal to 0,
	 - the second output tape contains all numbers from the input tape that
	   have bit at position bitnr equal to 1,
	   """
	
	output_tapes: list[list[int]] = [[], []]
	for i in input_tape:
		output_tapes[_test_int_bit(i, bit_nr)].append(i)
	
	bit_operator = operator.xor
	if len(output_tapes[0]) > len(output_tapes[1]):
		output_tapes[0], output_tapes[1] = output_tapes[1], output_tapes[0]
		bit_operator = operator.or_
	
	if len(output_tapes[0]) == 0:
		bit_operand = 1 << bit_nr
		missing = bit_operator(output_tapes[1][0], bit_operand)
		assert missing not in input_tape
		# print(f"Required {nr_bits - bit_nr} passes")
		return int(missing)
	else:
		return split_list(output_tapes[0], bit_nr - 1)

	
if __name__ == "__main__":

	def write_ints(start: int, stop: int, nr_ints: int, filename: str) -> None:
		"""Write nr_ints UNIQUE integers in range(start, stop) to filename."""
		
		with open(filename, "w") as f:
			for i in sample(range(start, stop, 1), nr_ints):
				f.write(str(i) + "\n")
	
	
	def read_ints(filename: str) -> list[int]:
		"""Return list of ints read from filename."""

		with open(filename) as f:
			return [int(i) for i in f]
	
	
	def main() -> None:
		"""Driver code."""

		filename = "_20bitints.txt"
		# write_ints(0, 2 ** 20, 1_000_000, filename)
		
		# input_tape = read_ints(filename)
		# print(len(input_tape))
		# print(input_tape)
		# print(sorted(input_tape))
		missing = split_tape(filename, 19)
		# assert missing not in input_tape
		print(missing)
		# print(len(list(get_all_missing(input_tape, 20))))

	main()
