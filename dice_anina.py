""" Dice problem Anina"""


class Dice(dict[str, str]):
	"""Simple class to mimic a dice. It can roll (in one of four directions at
	a time), its faces can be queried for their value, and it can produce a
	string representation of itself."""
	
	__transforms = {'L': "ULDRUFFBB", 'R': "RDLURFFBB",
	                'F': "UFDBULLRR", 'B': "BDFUBLLRR"}

	def __init__(self, faces: tuple[str, ...], values: tuple[str, ...]) -> None:
		super().__init__(zip(values, faces))
		self._faces_and_values = dict(zip(faces, values))
		
	def roll(self, direction: str) -> None:
		"""Roll in specified direction ('L', 'R', 'F', or 'D')."""
		
		transform = Dice.__transforms[direction]
		new_dice = dict(self)
		for value, current_face in self.items():
			new_dice[value] = transform[(transform.find(current_face) + 1)]
			self._faces_and_values[new_dice[value]] = value
		self.update(new_dice)
	
	def face_to_value(self, face: str) -> str:
		"""Return value at face (must be in ('U', 'D', 'L', 'R', 'F', 'B'))."""

		return self._faces_and_values[face]

	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__}({self})"


if __name__ == "__main__":

	dice = Dice(_faces := tuple('BRFULD'), _values := tuple('ABCDEF'))

	for roll_direction in 'LLFFRR':
		dice.roll(roll_direction)

	for _face in _faces:
		print(f"Value on {_face} face = {dice.face_to_value(_face)}")
