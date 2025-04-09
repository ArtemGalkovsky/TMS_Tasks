from dataclasses import dataclass
from random import uniform
from typing import Callable, Iterable
from config_vegetables import OptimalEnvironmentLevels
from main_config import (Number,
                         RANDOM_NUTRIENT_MIN_STRENGTH_LEVEL, RANDOM_NUTRIENT_MAX_STRENGTH_LEVEL,
                         RANDOM_NUTRIENT_MIN_REDUCTION_LEVEL, RANDOM_NUTRIENT_MAX_REDUCTION_LEVEL,
                         RANDOM_NUTRIENT_MIN_REDUCTION_MULTIPLIER, RANDOM_NUTRIENT_MAX_REDUCTION_MULTIPLIER,
                         RANDOM_LIGHT_MIN_LEVEL, RANDOM_LIGHT_MAX_LEVEL)
from utils import try_convert_str2int
from minor_classes import Lamp, Nutrient, Timer


@dataclass(frozen=True)
class LevelReport:
    is_in_normal_range: bool | None
    to_extremum_point_left: Number | None
    to_center_point_left: Number | None

    def __repr__(self):
        return (f"Level is optimal: {self.is_in_normal_range}; "
                f"To min/max based on value: {self.to_extremum_point_left}; "
                f"To center ((max-min)/2) point: {self.to_center_point_left}.")




class VegetableDiedException(Exception):
    pass

class Assistant:
    def __init__(self, name: str, job_position: str) -> None:
        self.name: str = name
        self.job_position: str = job_position

        self._current_working_object: Sample | None = None

    # TODO: Refactor this...
    def request_action(self):
        entered_valid_action: bool = False

        while not entered_valid_action:
            action = input("Enter action (sprinkle [s], fertilize [f], add light [l], Nothing to skip or exit [e]) ([x] - shorten action) > ").strip()

            if action == "":
                entered_valid_action = True
            elif action in ("exit", "e"):
                exit()
            elif action in ("sprinkle", "s"):
                to_sprinkle_level = try_convert_str2int(input("Enter the level to sprinkle > "))

                if to_sprinkle_level is not None:
                    self.sprinkle(to_sprinkle_level)
                    entered_valid_action = True
            elif action in ("fertilize", "f"):
                random_nutrient_approved = False

                while not random_nutrient_approved:
                    random_nutrient = Nutrient(
                        uniform(RANDOM_NUTRIENT_MIN_STRENGTH_LEVEL, RANDOM_NUTRIENT_MAX_STRENGTH_LEVEL),
                        uniform(RANDOM_NUTRIENT_MIN_REDUCTION_LEVEL, RANDOM_NUTRIENT_MAX_REDUCTION_LEVEL),
                        uniform(RANDOM_NUTRIENT_MIN_REDUCTION_MULTIPLIER, RANDOM_NUTRIENT_MAX_REDUCTION_MULTIPLIER)
                    )

                    print("You received a nutrient:", random_nutrient)

                    if input("Do you approve this nutrient? (y/n) ").lower() == "y":
                        self.add_nutrients(random_nutrient)
                        random_nutrient_approved = True
                        entered_valid_action = True

            elif action in ("add light", "l"):
                random_lamp_approved = False

                while not random_lamp_approved:
                    random_lamp = Lamp(
                        uniform(RANDOM_LIGHT_MIN_LEVEL, RANDOM_LIGHT_MAX_LEVEL),
                    )

                    print("You received a lamp:", random_lamp)

                    if input("Do you approve this lamp? (y/n) ").lower() == "y":
                        self.turn_on_light((random_lamp,))
                        random_lamp_approved = True
                        entered_valid_action = True


    def __str__(self):
        return f"Assistant {self.name} ({self.job_position})"


    def _check_if_current_object_exists(self) -> None:
        if self._current_working_object is None or not isinstance(self._current_working_object, Sample):
            raise RuntimeError(f"{self.__class__.__name__} {self.name} has no current working object! Or Object is not a Sample!")

    def sprinkle(self, water_level_to_sprinkle: Number) -> None:
        self._check_if_current_object_exists()

        self._current_working_object.add_water(water_level_to_sprinkle)

    def add_nutrients(self, nutrient: Nutrient) -> None:
        if not isinstance(nutrient, Nutrient):
            raise TypeError("nutrient must be of type Nutrient.")

        self._check_if_current_object_exists()
        self._current_working_object.add_nutrients(nutrient)

    def turn_on_light(self, lamps: Iterable[Lamp]) -> None:
        self._check_if_current_object_exists()

        if not all(isinstance(lamp, Lamp) for lamp in lamps):
            raise ValueError("lamps must be of type Lamp.")

        self._current_working_object.add_more_light(lamps)

    def focus_on_object(self, object_: "Sample") -> None:
        if not isinstance(object_, Sample):
            raise ValueError("object_ must be an instance of Sample.")

        self._current_working_object = object_

    def get_raw_object_info(self) -> dict[str: dict[str, Number | str], str: dict[str, LevelReport | bool]]:
        return {
            "vegetable_info": self._current_working_object.get_vegetable_info(),
            "sample_info": self._current_working_object.check_sample()
        }

    def _add_levels_hint(self, report: LevelReport) -> Number | None:
        if isinstance(report, LevelReport) and report.to_extremum_point_left >= 0:
            return report.to_extremum_point_left

        return 0



    def get_object_info(self) -> str:
        raw_info = self.get_raw_object_info()

        vegetable_info = raw_info.get("vegetable_info", {})
        sample_info = raw_info.get("sample_info", {})

        report_water = sample_info.get("water_level", "undefined")
        report_nutrients = sample_info.get("nutrients_level", "undefined")
        report_light = sample_info.get("light_level", "undefined")

        lamps = ""
        for lamp in sample_info.get("lamps", ()):
            lamps += f"{lamp}\n"

        return f"""Vegetable {vegetable_info.get("type", "Unknown Type")}:
    Water level: {vegetable_info.get("water_level", "undefined")}
    Nutrients level: {vegetable_info.get("nutrients_level", "undefined")}
    Light level: {vegetable_info.get("light_level", "undefined")}
    Drought level per hour: {vegetable_info.get("drought_level_per_hour", "undefined")}

Sample Reports:
    Water level: {report_water}
    Nutrients level: {report_nutrients}
    Light level: {report_light}

Lamps:
{lamps}
To do:
    Sprinkle +-{self._add_levels_hint(report_water)} water levels,
    Add nutrients: +-{self._add_levels_hint(report_nutrients)} nutrients levels.
    Turn on lamp to add: +-{self._add_levels_hint(report_light)} light levels.
----------"""


def verify_vegetable_levels_after_function_complete(func: Callable) -> Callable:
    def wrapper(self: "Vegetable", *args, **kwargs):
        func_output = func(self, *args, **kwargs)

        for level_value in (self._water_level, self._nutrients_level, self._light_level):
            if level_value < 0.1 or level_value > 100:
                raise VegetableDiedException(f"{self._type} DIED! {self.info()}")

        return func_output

    return wrapper


class Vegetable:
    @verify_vegetable_levels_after_function_complete
    def __init__(self, start_water_level: Number, start_nutrients_level: Number,
                 start_light_level: Number, drought_level_per_hour: Number = 5, nutrient: Nutrient | None = None) -> None:
        self._type: str = self.__class__.__name__

        self._water_level: Number = start_water_level
        self._drought_level_per_hour: Number = drought_level_per_hour

        self._light_level: Number = start_light_level
        self._nutrients_level: Number = start_nutrients_level


        self._nutrients: list[Nutrient] = []
        if nutrient is not None:
            self.add_nutrition(nutrient)


    @property
    def water_level(self) -> Number:
        return self._water_level

    @verify_vegetable_levels_after_function_complete
    def change_water_level(self, water_level: Number) -> None:
        self._water_level += water_level

    @property
    def nutrients_level(self) -> Number:
        return self._nutrients_level

    def add_nutrition(self, nutrient: Nutrient) -> None:
        if not isinstance(nutrient, Nutrient):
            raise ValueError("nutrient must be an instance of Nutrient.")

        self._nutrients.append(nutrient)
        self.update_self(0)

    @property
    def light_level(self) -> Number:
        return self._light_level

    @verify_vegetable_levels_after_function_complete
    def set_light_level(self, light_level: Number) -> None:
        self._light_level = light_level

    def raw_info(self) -> dict[str, Number | str]:
        return {
            "type": self._type,
            "water_level": self._water_level,
            "nutrients_level": self._nutrients_level,
            "light_level": self._light_level,
            "drought_level_per_hour": self._drought_level_per_hour,
        }

    def info(self) -> str:
        raw_info = self.raw_info()

        return f"""Vegetable {raw_info.get('type', 'Unknown Type')}:
    Water level: {raw_info.get('water_level', 'undefined')},
    Nutrients level: {raw_info.get('nutrients_level', 'undefined')},
    Light level: {raw_info.get('light_level', 'undefined')}."""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.info()}"


    def update_self(self, hours_past: int) -> None:
        if not isinstance(hours_past, int):
            raise TypeError("hours_past must be an int.")

        self.change_water_level(-self._drought_level_per_hour * hours_past)

        new_nutrients_level = 0
        for nutrient in self._nutrients:
            new_nutrients_level += nutrient.get_nutrients_strength_for_hours_past(hours_past)

        self._nutrients_level = new_nutrients_level


class Sample:
    def __init__(self, vegetable: Vegetable, optimal_levels: OptimalEnvironmentLevels, lamps: Iterable[Lamp]) -> None:
        self._vegetable: Vegetable = vegetable
        self.optimal_levels: OptimalEnvironmentLevels = optimal_levels
        self._lamps: list[Lamp] = []

        self.add_more_light(lamps)

    def get_vegetable_info(self) -> dict[str, Number | str]:
        return self._vegetable.raw_info()

    def check_sample(self) -> dict[str, LevelReport | bool]:
        def check_one_position(attribute_min_name: str, attribute_max_name: str, current_level: Number) -> LevelReport:
            to_extremum_point_left = 0
            is_in_normal_range = False

            attribute_min_value = self.optimal_levels.__getattribute__(attribute_min_name)
            attribute_max_value = self.optimal_levels.__getattribute__(attribute_max_name)

            if attribute_min_value > current_level:
                to_extremum_point_left = attribute_min_value - current_level
            elif attribute_max_value < current_level:
                to_extremum_point_left = attribute_max_value - current_level
            else:
                is_in_normal_range = True

            center_point = (attribute_max_value + attribute_max_value) / 2
            to_center_point_left = center_point - current_level

            return LevelReport(is_in_normal_range, to_extremum_point_left, to_center_point_left)

        water_level_report = check_one_position(
            "water_level_min",
            "water_level_max",
            self._vegetable.water_level
        )

        nutrients_level_report = check_one_position(
            "nutrients_level_min",
            "nutrients_level_max",
            self._vegetable.nutrients_level
        )

        light_level_report = check_one_position(
            "light_level_min",
            "light_level_max",
            self._vegetable.light_level
        )

        return {
            "water_level": water_level_report,
            "nutrients_level": nutrients_level_report,
            "light_level": light_level_report,
            "all_values_are_normal": all((water_level_report.is_in_normal_range,
                                          nutrients_level_report.is_in_normal_range,
                                          light_level_report.is_in_normal_range)),
            "lamps": tuple(self._lamps)
        }

    def add_water(self, water_level: Number) -> None:
        if water_level < 0:
            raise ValueError("Water level cannot be negative")

        self._vegetable.change_water_level(water_level)

    def add_nutrients(self, nutrient: Nutrient) -> None:
        if not isinstance(nutrient, Nutrient):
            raise TypeError("nutrient must be an Nutrient.")

        self._vegetable.add_nutrition(nutrient)

    def add_more_light(self, lamps: Iterable[Lamp]) -> None:
        if not all(isinstance(lamp, Lamp) for lamp in lamps):
            raise ValueError("lamps must be of type Lamp.")

        self._lamps.extend(lamps)

    def update_sample_stats(self, hours_past: int) -> None:
        if not isinstance(hours_past, int):
            raise TypeError("hours_past must be an int.")

        for _ in range(hours_past):
            for lamp in self._lamps:
                lamp.update_self(1)

            self._vegetable.update_self(1)

        self._vegetable.set_light_level(
            sum(lamp.light_level for lamp in self._lamps)
        )



__all__ = ["Vegetable", "Sample", "Assistant", "VegetableDiedException", "Timer", "Nutrient", "Lamp"]

if __name__ == '__main__':
    from config_vegetables import OPTIMAL_ENVIRONMENT_LEVELS

    vegetable = Vegetable(10, 10, 10)
    print(vegetable)

    sample = Sample(vegetable, OPTIMAL_ENVIRONMENT_LEVELS["Corn"])
    print(sample.check_sample())

    assistant = Assistant("John", "Main Specialist")
    assistant.focus_on_object(sample)
    assistant.sprinkle(1)

    day_timer = Timer(0)
    day_timer.connect_update_function(vegetable.update_self)

    for hour in range(48):
        print("----------------------------\n")
        print(assistant.get_object_info())
        day_timer.add_hours()
        print(assistant.get_object_info())




