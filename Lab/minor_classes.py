from main_config import Number, LAMP_BREAK_CHANCE_MAX
from random import uniform
from typing import Callable


class Nutrient:
    def __init__(self, nutrients_strength: Number, start_reduction_value: Number = 5, reduction_per_hour_multiplier: Number = 2) -> None:
        self._current_nutrients_strength: Number = nutrients_strength
        self._current_reduction_value: Number = start_reduction_value
        self._reduction_per_hour_multiplier: Number = reduction_per_hour_multiplier


    def get_nutrients_strength_for_hours_past(self, hours_past: int = 1) -> Number:
        if not isinstance(hours_past, int):
            raise ValueError("hours_past must be an integer")

        for hour in range(hours_past):
            self._current_nutrients_strength -= self._current_reduction_value
            self._current_reduction_value *= self._reduction_per_hour_multiplier

        return self._current_nutrients_strength

    def __str__(self) -> str:
        return f"Nutrient with current strength {self._current_nutrients_strength}, reduction level: {self._current_reduction_value} and reduction per hour multiplier: {self._reduction_per_hour_multiplier}"


class Lamp:
    def __init__(self, light_level: Number):
        self._light_level: Number = light_level
        self._break_chance: Number = uniform(1, LAMP_BREAK_CHANCE_MAX)

        self._is_broken: bool = False

    @property
    def is_broken(self) -> bool:
        return self._is_broken

    @property
    def break_chance(self) -> Number:
        return self._break_chance

    @property
    def light_level(self) -> Number:
        if self._is_broken:
            return 0

        return self._light_level

    def update_self(self, hours_past: int) -> None:
        if self._is_broken:
            return

        if not isinstance(hours_past, int):
            raise ValueError("hours_past must be an integer")

        for _ in range(hours_past):
            if uniform(0, 100) < self.break_chance:
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!One lamp broke!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

                self._is_broken = True
                return

    def __str__(self) -> str:
        return f"Lamp with {self._light_level} light level and break chance: {self.break_chance}."

class Timer:
    def __init__(self, current_hour: int, day_length_hours: int = 24) -> None:
        self._days_past: int = 0

        if not isinstance(current_hour, int):
            raise TypeError("current_hour must be of type int.")

        if not isinstance(current_hour, int):
            raise TypeError("day_length_hours must be of type int.")

        self._current_hour: int = current_hour
        self._day_length_hours: int = day_length_hours

        self._update_functions = []

    def update(self):
        self._update_all(0)

    def add_hours(self, hours: int = 1):
        if not isinstance(hours, int) or hours < 0:
            raise ValueError("hours must be a non-negative integer")

        total_hours = self._current_hour + hours
        days_to_add = total_hours // self._day_length_hours
        self._current_hour = total_hours % self._day_length_hours
        self._days_past += days_to_add

        self._update_all(hours)

    def _update_all(self, hours_past: int) -> None:
        for function in self._update_functions:
            function(hours_past)

    @property
    def current_hour(self) -> Number:
        return self._current_hour

    @property
    def days_past(self) -> int:
        return self._days_past

    @property
    def day_length_hours(self) -> Number:
        return self._day_length_hours

    def connect_update_function(self, function: Callable) -> None:
        self._update_functions.append(function)

    def disconnect_update_function(self, function: Callable) -> None:
        if function in self._update_functions:
            self._update_functions.remove(function)