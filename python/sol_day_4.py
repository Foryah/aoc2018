from datetime import datetime
from halo import Halo
from utils import load_input
from typing import List, Dict, Tuple

DAY_INPUT = "../inputs/day4a"


class NoteAnalyzer:
    GUARD_TAG = "Guard #"
    FALLS_ASLEEP = "falls asleep"
    WAKES_UP = "wakes up"

    @staticmethod
    def extract_date(note: str) -> datetime:
        # format: [year-month-day hour:minute] additional_info
        date_str = note.split("[")[1].split("]")[0]
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return date

    @staticmethod
    def extract_guard_id(note: str) -> int:
        # format: Guard #number begins shift
        id_str = note.split(NoteAnalyzer.GUARD_TAG)[1].split(" ")[0]
        return int(id_str)

    @staticmethod
    def is_guard_shift(note: str) -> bool:
        return NoteAnalyzer.GUARD_TAG in note

    @staticmethod
    def is_falling_asleep(note: str) -> bool:
        return NoteAnalyzer.FALLS_ASLEEP in note

    @staticmethod
    def is_waking_up(note: str) -> bool:
        return NoteAnalyzer.WAKES_UP in note


class Guard:
    def __init__(self, guard_id: int, guard_notes: List[str]):
        self._guard_notes = guard_notes
        self._id = guard_id
        self._behaviour = self._analyze_notes()

    def _analyze_notes(self) -> Dict[str, Dict[int, int]]:
        # This function works under the assumption that
        # a quard is always awake before his/her shift
        # ends. In other words, the last note for a guard
        # cannot be that it falls asleep.
        behaviour: Dict[str, Dict[int, int]] = {}

        notes_to_analyze = self._guard_notes[::]

        while notes_to_analyze:
            note = notes_to_analyze.pop(0)
            try:
                # Since pop removes the note, now 0 is the next one
                next_note = notes_to_analyze[0]
            except IndexError:
                if NoteAnalyzer.is_guard_shift(note):
                    continue
                else:
                    raise Exception("Huston we have a problem!")

            if NoteAnalyzer.is_guard_shift(note):
                # At this point we have no idea if the guard
                # was asleep or awake when the shift started
                if NoteAnalyzer.is_waking_up(next_note):
                    # This means he was asleep all this time
                    started_sleeping = NoteAnalyzer.extract_date(note)
                    stoped_sleeping = NoteAnalyzer.extract_date(next_note)
                    self.__set_asleep(started_sleeping, stoped_sleeping, behaviour)
                    # Remove the next note to not process it again
                    notes_to_analyze.pop(0)
                elif NoteAnalyzer.is_falling_asleep(next_note):
                    # This means he/she was awake until this point
                    continue
                elif NoteAnalyzer.is_guard_shift(next_note):
                    # Two guard shifts means the shift was all awake?
                    continue
                else:
                    raise Exception("WTF?")
            elif NoteAnalyzer.is_falling_asleep(note):
                if NoteAnalyzer.is_waking_up(next_note):
                    started_sleeping = NoteAnalyzer.extract_date(note)
                    stoped_sleeping = NoteAnalyzer.extract_date(next_note)
                    self.__set_asleep(started_sleeping, stoped_sleeping, behaviour)
                    # Remove the next note to not process it again
                    notes_to_analyze.pop(0)
                else:
                    raise Exception("Undefined behavior: falls asleep but doesn't wake up")
            else:
                raise Exception("Cannot be!")

        return behaviour

    def __set_asleep(self, start_date: datetime, end_date: datetime, behaviour: Dict[str, Dict[int, int]]):
        def set_date_and_hour(month_and_day: str, minute: int, behaviour: Dict[str, Dict[int, int]]):
            if month_and_day in behaviour:
                behaviour[month_and_day][minute] = 1
            else:
                behaviour[month_and_day] = {minute: 1}

        month_and_day = "{}-{}".format(start_date.month, start_date.day)
        for minute in range(start_date.minute, end_date.minute, 1):
            set_date_and_hour(month_and_day, minute, behaviour)

    @property
    def id(self) -> int:
        return self._id

    @property
    def sleep_time(self) -> int:
        return sum([len(values.keys()) for day, values in self._behaviour.items()])

    def get_sleepiest_minute(self) -> Tuple[int, int]:
        all_minutes = [0 for _ in range(60)]
        for _, data in self._behaviour.items():
            for minute, value in data.items():
                all_minutes[minute] += value

        max_time = max(all_minutes)
        minute = all_minutes.index(max_time)
        return minute, max_time


class Log:
    def __init__(self, notes: List[str]):
        self._notes = notes

    def _sort_notes(self) -> List[str]:
        sorted_notes = self._notes[::]
        sorted_notes.sort(key=NoteAnalyzer.extract_date)

        return sorted_notes

    @property
    def guards_notes(self) -> Dict[int, List[str]]:
        sorted_notes = self._sort_notes()

        guards_notes: Dict[int, List[str]] = {}
        current_guard_id: int
        for note in sorted_notes:
            if NoteAnalyzer.is_guard_shift(note):
                current_guard_id = NoteAnalyzer.extract_guard_id(note)

            if current_guard_id in guards_notes:
                guards_notes[current_guard_id].append(note)
            else:
                guards_notes[current_guard_id] = [note]

        return guards_notes


def set_up(input_data: str) -> Tuple[Log, List[Guard]]:
    log = Log(input_data.split("\n"))

    guards: List[Guard] = []
    for guard_id, guard_notes in log.guards_notes.items():
        guards.append(Guard(guard_id, guard_notes))

    return log, guards


@Halo(text="Solving first part...", placement="right")
def solve_first_part(guards: List[Guard]) -> int:
    worst_guard = guards[0]
    most_sleep_time: int = guards[0].sleep_time
    for guard in guards[1:]:
        if most_sleep_time < guard.sleep_time:
            most_sleep_time = guard.sleep_time
            worst_guard = guard

    sleepiest_minute, _ = worst_guard.get_sleepiest_minute()
    return worst_guard.id * sleepiest_minute


@Halo(text="Solving second part...", placement="right")
def solve_second_part(guards: List[Guard]) -> int:
    worst_guard = guards[0]
    _, sleepiest_minute_time = guards[0].get_sleepiest_minute()
    for guard in guards[1:]:
        _, guard_sleepiest_minute_time = guard.get_sleepiest_minute()
        if sleepiest_minute_time < guard_sleepiest_minute_time:
            sleepiest_minute_time = guard_sleepiest_minute_time
            worst_guard = guard

    worst_sleepiest_minute, _ = worst_guard.get_sleepiest_minute()
    return worst_guard.id * worst_sleepiest_minute


if __name__ == "__main__":
    log, guards = set_up(load_input(DAY_INPUT))

    first_sol = solve_first_part(guards)
    print(f"First part solution: {first_sol}")

    second_sol = solve_second_part(guards)
    print(f"Second part solution: {second_sol}")
