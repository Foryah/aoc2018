from utils import load_input
from halo import Halo
from typing import Any, Dict, Tuple

DAY_INPUT = "../inputs/day2a"


@Halo(text="Solving first part...", placement="right")
def solve_first_part(input_data: str) -> int:
    def histogram(_input: Any) -> Dict[str, int]:
        histogram = {}

        input_clone = _input[::]
        while input_clone:
            elem = input_clone[0]
            histogram[elem] = input_clone.count(elem)

            input_clone = [i for i in input_clone if i != elem]

        return histogram

    twos, threes = 0, 0
    for _input in input_data.splitlines():
        input_hist = histogram(_input)

        has_twos = 2 in input_hist.values()
        has_threes = 3 in input_hist.values()

        twos += 1 if has_twos else 0
        threes += 1 if has_threes else 0

    return twos * threes


@Halo(text="Solving second part...", placement="right")
def solve_second_part(input_data: str) -> str:
    def max_1_difference(first_val: str, second_val: str) -> Tuple[bool, Any]:
        NO_DIFF = -1
        diff_index = NO_DIFF

        for index, letter in enumerate(first_val):
            if letter != second_val[index]:
                if diff_index == NO_DIFF:
                    diff_index = index
                else:
                    return False, None

        return True, diff_index

    data_list = input_data.splitlines()
    for index, item in enumerate(data_list):
        for next_item in data_list[index + 1 :]:
            has_diff, diff_index = max_1_difference(item, next_item)
            if has_diff:
                return item[:diff_index] + item[diff_index + 1 :]

    raise Exception("No solution found!")


if __name__ == "__main__":
    first_sol = solve_first_part(load_input(DAY_INPUT))
    print(f"First part solution: {first_sol}")

    second_sol = solve_second_part(load_input(DAY_INPUT))
    print(f"Second part solution: {second_sol}")
