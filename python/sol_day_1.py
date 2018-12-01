from itertools import cycle
from halo import Halo


def load_input(path: str = "../inputs/day1a") -> str:
    with open(path, "r") as f:
        return f.read().rstrip()


@Halo(text="Solving first part...", placement="right")
def solve_first_part(input_data: str) -> int:
    expression = input_data.replace("\n", "")
    return eval(expression)


@Halo(text="Solving second part...", placement="right")
def solve_second_part(input_data: str) -> int:
    change_list = input_data.split("\n")

    frequencies = [0]
    current_frequency = 0
    for change in cycle(change_list):
        current_frequency = eval(f"{current_frequency}{change}")

        if current_frequency in frequencies:
            return current_frequency

        frequencies.append(current_frequency)


if __name__ == "__main__":
    first_sol = solve_first_part(load_input())
    print(f"First part solution: {first_sol}")

    second_sol = solve_second_part(load_input())
    print(f"Second part solution: {second_sol}")
