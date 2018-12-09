from utils import load_input
from halo import Halo
from typing import Tuple, List

DAY_INPUT = "../inputs/day5a"


class PolymerHandler:
    @staticmethod
    def get_units(polymer: str) -> List[str]:
        all_units: List[str] = []
        for unit in polymer:
            if unit.lower() not in all_units:
                all_units.append(unit.lower())

        return all_units

    @staticmethod
    def fully_react(polymer: str) -> int:
        had_reaction = True
        while had_reaction:
            polymer, had_reaction = PolymerHandler.__react(polymer)

        return len(polymer)

    @staticmethod
    def remove_unit(polymer: str, unit: str) -> str:
        return "".join([u for u in polymer if u not in [unit.lower(), unit.upper()]])

    @staticmethod
    def __are_oposite(first_unit: str, second_unit: str) -> bool:
        same_unit_type = first_unit.lower() == second_unit.lower()
        first_up_second_low = first_unit.isupper() and second_unit.islower()
        first_low_second_up = first_unit.islower() and second_unit.isupper()
        return same_unit_type and (first_up_second_low or first_low_second_up)

    @staticmethod
    def __react(polymer: str) -> Tuple[str, bool]:
        had_reaction = False
        index = 0
        while index < len(polymer) - 1:
            unit = polymer[index]
            next_unit = polymer[index + 1]

            if PolymerHandler.__are_oposite(unit, next_unit):
                polymer = polymer[:index] + polymer[index + 2 :]
                index = index - 1 if index != 0 else index

                if not had_reaction:
                    had_reaction = True
            else:
                index += 1

        return polymer, had_reaction


@Halo(text="Solving first part...", placement="right")
def solve_first_part(polymer: str) -> int:
    return PolymerHandler.fully_react(polymer)


@Halo(text="Solving second part...", placement="right")
def solve_second_part(polymer: str) -> Tuple[int, str]:
    all_units = PolymerHandler.get_units(polymer)

    lowest_count = len(polymer)
    best_unit = all_units[0]
    for unit in all_units:
        simplified_polymer = PolymerHandler.remove_unit(polymer, unit)
        count = PolymerHandler.fully_react(simplified_polymer)

        if count < lowest_count:
            lowest_count = count
            best_unit = unit

    return lowest_count, best_unit


if __name__ == "__main__":
    units_count = solve_first_part(load_input(DAY_INPUT))
    print(f"First part solution: {units_count}")

    units_count, unit = solve_second_part(load_input(DAY_INPUT))
    print(f"Second part solution: {units_count} {unit}")
