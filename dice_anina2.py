"""A somewhat smaller version (not a class)..."""
from typing import Optional

transforms = ("LDRUL", "RDLUR", "FDBUF", "BDFUB")


def get_transform(direction: str) -> Optional[str]:
	"""Return the transform for the given direction."""

	for transform in transforms:
		if transform[0] == direction:
			return transform
	return None


def find_next_face(transform: str, current_face: str) -> str:
	"""Return the next face of the current face according to given transform."""

	for offset, face in enumerate(transform):
		if face == current_face:
			return transform[offset + 1]
	return current_face


def roll(dice: list[list[str]], direction: str) -> None:
	"""Process roll in given direction on given dice."""

	for value_face in dice:
		value_face[1] = find_next_face(get_transform(direction), value_face[1])

if __name__ == "__main__":
	
	def _main() -> None:
		dice = [[*"CF"], [*"BR"], [*"AB"], [*"FD"], [*"EL"], [*"DU"]]
	
		for _roll in "LLFFRR":
			roll(dice, _roll)
		
		for value_face in dice:
			print(f"Value on {value_face[1]} face = {value_face[0]}")
		
	_main()
