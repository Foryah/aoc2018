from utils import load_input
from halo import Halo
from typing import Dict, Tuple, List, Any

DAY_INPUT = "../inputs/day3a"


class Coordinates:
    def __init__(self, x: Any, y: Any):
        self._x = int(x)
        self._y = int(y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def to_tuple(self):
        return (self._x, self._y)

    def absolute(self, size: "Coordinates") -> List["Coordinates"]:
        coordinates: List[Coordinates] = []
        for x_offset in range(size.x):
            for y_offset in range(size.y):
                coordinates.append(Coordinates(self._x + x_offset, self._y + y_offset))

        return coordinates


class Claim:
    def __init__(self, definition: str):
        self.definition = definition
        self.__init_from_definition()

    def __init_from_definition(self):
        # Input looks like: #1 @ 1,3: 4x4 -> #id @ position(x,y): size(x,y)
        position_coords = self.definition.split("@")[1].split(":")[0].strip().split(",")
        size = self.definition.split("@")[1].split(":")[1].strip().split("x")

        self.id = self.definition.split("@")[0].strip()
        self.position = Coordinates(*position_coords)
        self.size = Coordinates(*size)
        self.absolute_coords = self.position.absolute(self.size)


class Fabirc:
    def __init__(self):
        self._fabric: Dict[Tuple[int, int], int] = {}

    def add(self, claim: Claim):
        for coords in claim.absolute_coords:
            coords_tuple = coords.to_tuple()

            if coords_tuple in self._fabric:
                self._fabric[coords_tuple] += 1
            else:
                self._fabric[coords_tuple] = 1

    def get_overlap(self):
        return [coords for coords, count in self._fabric.items() if count > 1]

    def get_no_overlap(self):
        return [coords for coords, count in self._fabric.items() if count == 1]


@Halo(text="Solving first part...", placement="right")
def solve_first_part(input_data: str) -> Tuple[Fabirc, List[Claim]]:
    fabric = Fabirc()
    claims = []
    for _input in input_data.splitlines():
        claim = Claim(_input)

        fabric.add(claim)
        claims.append(claim)

    return fabric, claims


@Halo(text="Solving second part...", placement="right")
def solve_second_part(fabric: Fabirc, claims: List[Claim]) -> str:
    no_overlap = fabric.get_no_overlap()
    for claim in claims:
        broken_claim = False
        for coord in claim.absolute_coords:
            if coord.to_tuple() not in no_overlap:
                broken_claim = True
                break

        if not broken_claim:
            return claim.id

    raise Exception("No solution found!")


if __name__ == "__main__":
    fabric, claims = solve_first_part(load_input(DAY_INPUT))
    overlap_count = len(fabric.get_overlap())
    print(f"First part solution: {overlap_count}")

    second_sol = solve_second_part(fabric, claims)
    print(f"Second part solution: {second_sol}")
