""" Dice problem Anina"""


class Dice(dict[str, str]):
	"""Simple class to mimic a dice. It can roll (in one of four directions at
	a time), its faces can be queried for their values, and it can produce a
	string representation of itself."""
	
	__faces = 'UDLRFB'
	__transforms = {'L': "ULDRUFFBB", 'R': "RDLURFFBB", 'F': "UFDBULLRR",
	                'B': "BDFUBLLRR"}

	def __init__(self, faces: tuple[str, ...], values: tuple[str, ...]) -> None:
		super().__init__(zip(values, faces))
		self._faces_and_values = dict(zip(faces, values))
		
	def roll(self, roll: str) -> None:
		"""Roll in specified direction ('L', 'R', 'F', or 'D')."""
		
		transform = self.__transforms[roll]
		new_dice = dict(self)
		for value, current_face in self.items():
			new_dice[value] = transform[(transform.find(current_face) + 1)]
			self._faces_and_values[new_dice[value]] = value
		self.update(new_dice)
	
	def face_to_value(self, face: str) -> str:
		"""Return the current value at face. Face is expected to be in
		('U', 'D', 'L', 'R', 'F', 'B')."""

		return self._faces_and_values[face]

	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__}({self})"


if __name__ == "__main__":

	dice = Dice(_faces := tuple('BRFULD'), _values := tuple('ABCDEF'))

	for _roll in 'LLFFRR':
		dice.roll(_roll)

	for _face in _faces:
		print(f"Value on {_face} face = {dice.face_to_value(_face)}")
