""" Dice problem Anina"""
from __future__ import annotations
from typing import Optional

faces = ('UP', 'DOWN', 'LEFT', 'RIGHT', 'FRONT', 'BACK')


class Dice:
	"""Simple class to mimic a dice. It can roll (in one of four directions at
	a time), its faces can be queried for their values, and it can produce a
	string representation of itself."""
	
	__transformations = {'L': "ULDR", 'R': "RDLU", 'F': "UFDB", 'B': "BDFU"}

	def __init__(self, values_and_faces: dict[str, str]) -> None:
		self._values_and_faces = values_and_faces

	def roll(self, roll: str) -> None:
		"""Roll in specified direction ('L', 'R', 'F', or 'D')."""
		
		transformation = self.__transformations[roll]
		new_dice = dict()
		new_dice.update(self._values_and_faces)
		for value, current_face in self._values_and_faces.items():
			if (current_face_index := transformation.find(current_face)) != -1:
				new_dice[value] = transformation[(current_face_index + 1) % 4]
		self._values_and_faces = new_dice

	def get_face_value(self, face: str) -> Optional[str]:
		"""Return the current value at face (or None if face invalid)."""
		
		for value, _face in self._values_and_faces.items():
			if face[0] == _face:
				return value
		return None

	def __str__(self) -> str:
		return '\n'.join(f"letter on {face} face = "
		                 f"{self.get_face_value(face)}"
		                 for face in faces)
	
	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__}({self._values_and_faces})"


if __name__ == "__main__":

	dice = Dice({'A': 'B', 'B': 'R', 'C': 'F', 'D': 'U', 'E': 'L', 'F': 'D'})

	for _roll in "LLFFRR":
		dice.roll(_roll)

	face_to_query = 'UP'     # we are interested in value at 'UP' face.
	print(f"Current letter on {face_to_query} side of the dice: "
	      f"{dice.get_face_value(face_to_query)}")
	print(dice)
