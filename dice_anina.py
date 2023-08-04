""" Dice problem Anina"""


class Dice:
	"""Simple class to mimic a dice. It can roll (in one of four directions at
	a time), its faces can be queried for their values, and it can produce a
	string representation of itself."""
	
	__faces = 'UDLRFB'
	__transforms = {'L': "ULDRUFFBB", 'R': "RDLURFFBB", 'F': "UFDBULLRR",
	                'B': "BDFUBLLRR"}

	def __init__(self, faces_2_values: dict[str, str]) -> None:
		self._dice = {v: k for (k, v) in faces_2_values.items()}
		self._modified = True
		self._faces_and_values = dict(faces_2_values)
		
	def roll(self, roll: str) -> None:
		"""Roll in specified direction ('L', 'R', 'F', or 'D')."""
		
		transform = self.__transforms[roll]
		new_dice = dict(self._dice)
		for value, current_face in self._dice.items():
			new_dice[value] = transform[(transform.find(current_face) + 1)]
		self._dice = new_dice
		self._modified = True
		
	def get_face_value(self, face: str) -> str:
		"""Return the current value at face (or None if face invalid)."""

		if self._modified:
			self._faces_and_values = {v: k for (k, v) in self._dice.items()}
			self._modified = False
		return self._faces_and_values[face]

	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__}({self._dice})"


if __name__ == "__main__":

	dice = Dice(dict(zip("BRFULD", "ABCDEF")))

	for _roll in "LLFFRR":
		dice.roll(_roll)

	for _face in 'UDLRFB':
		print(f"Current letter on {_face} side = {dice.get_face_value(_face)}")
