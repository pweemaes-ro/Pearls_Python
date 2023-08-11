"""Test for both the functional and class version of the dice sim."""
from random import choice

from dice_anina import Dice
from dice_anina2 import roll

directions = "LRFB"
roll_inverse = {"L": "R", "R": "L", "F": "B", "B": "F"}


def _generate_symmetric_rolls(half_length: int) -> str:
	"""Return s rolls string that results in 'identity-roll', by first doing a
	number of rolls and then inverting (undo-ing) them."""
	
	half = ''.join(choice(directions) for _ in range(half_length))
	return half + ''.join(roll_inverse[k] for k in half[::-1])


def test_dice_rolls_class() -> None:
	original_dice_class = \
		Dice(_faces := tuple('BRFULD'), _values := tuple('ABCDEF'))
	dice_class = \
		Dice(_faces := tuple('BRFULD'), _values := tuple('ABCDEF'))

	# do the rolls
	for test_roll in ("L" * 4, "R" * 4, "F" * 4, "B" * 4):
		for roll_direction in test_roll:
			dice_class.roll(roll_direction)
		assert dice_class == original_dice_class

	for i in range(10):
		test_roll = _generate_symmetric_rolls(15)
		for roll_direction in test_roll:
			dice_class.roll(roll_direction)
		assert dice_class == original_dice_class


def test_dice_rolls_functional() -> None:
	original_dice_functional = \
		[[*"CF"], [*"BR"], [*"AB"], [*"FD"], [*"EL"], [*"DU"]]
	dice_functional = \
		[[*"CF"], [*"BR"], [*"AB"], [*"FD"], [*"EL"], [*"DU"]]

	# do the rolls
	for test_roll in ("L" * 4, "R" * 4, "F" * 4, "B" * 4):
		for roll_direction in test_roll:
			roll(dice_functional, roll_direction)
		assert dice_functional == original_dice_functional

	for i in range(10):
		test_roll = _generate_symmetric_rolls(15)
		for roll_direction in test_roll:
			roll(dice_functional, roll_direction)
		assert dice_functional == original_dice_functional
