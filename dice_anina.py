""" Dice problem Anina"""
from typing import Any


class Dice(dict[str, str]):
	"""A dice has 6 faces: Up (U), down (D), left (L), right (R), front (F) and
	back (B). It can roll to left (L), right (R), front(F) or back (B). Its
	faces can be queried for their value."""
	
	# Transform strings describe changes for a given roll: For each face, find
	# the 1st occurence of its letter. The next letter is the next location. So
	# 'L': "ULDRU" means: a left roll brings value at U face to L face, value
	# at L face to D face, value at D face to R face, and value at R face to U
	# face. Values at F and B faces DON'T move!
	__transforms = {'L': "LDRUL", 'R': "RDLUR", 'F': "FDBUF", 'B': "BDFUB"}

	def __init__(self, faces: tuple[str, ...], values: tuple[str, ...]) -> None:
		super().__init__(zip(values, faces))
		# Besides a dict with values as keys and faces as values, we also
		# maintain a dict with faces as keys and values as values (for quick
		# lookup of a face's value).
		self._faces_2_values = dict(zip(faces, values))
		
	def roll(self, direction: str) -> None:
		"""Roll in specified direction ('L', 'R', 'F', or 'D')."""
		
		transform = Dice.__transforms[direction]
		new_dice = dict(self)
		for value, current_face in self.items():
			if (current_face_idx := transform.find(current_face)) != -1:
				# process transform in both (!) dictionaries.
				new_dice[value] = transform[current_face_idx + 1]
				self._faces_2_values[new_dice[value]] = value
		self.update(new_dice)
	
	def face_to_value(self, face: str) -> str:
		"""Return value at face (face in ('U', 'D', 'L', 'R', 'F', 'B'))."""

		return self._faces_2_values[face]

	def __eq__(self, other: Any) -> bool:
		if isinstance(other, Dice):
			return self.items() == other.items()
		else:
			return False


if __name__ == "__main__":

	# create dice
	dice = Dice(_faces := tuple('BRFULD'), _values := tuple('ABCDEF'))

	# do the rolls
	for roll_direction in 'LLFFRR':
		dice.roll(roll_direction)

	# print face values for all faces.
	for _face in _faces:
		print(f"Value on {_face} face = {dice.face_to_value(_face)}")
