from random import randrange
from main_classes import Vegetable, Sample, Nutrient, Lamp
from config_vegetables import OPTIMAL_ENVIRONMENT_LEVELS
from main_config import Number

class CustomizableLamp(Lamp):
    def __init__(self, light_level: Number, break_chance_max: Number):
        super().__init__(light_level)

        self._break_chance: Number = randrange(1, break_chance_max+1)

# TODO: WTFFFFFFFFFFFFFFFFFFFFFFFFFFFFF. TO MUCH OOP

class Corn(Vegetable):
    def __init__(self, start_water_level: Number, start_nutrients_level: Number, start_light_level: Number,
                 drought_level_per_hour: Number = 5, nutrient: Nutrient | None = None):
        super().__init__(start_water_level, start_nutrients_level, start_light_level, drought_level_per_hour, nutrient)


class Tomato(Vegetable):
    def __init__(self, start_water_level: Number, start_nutrients_level: Number, start_light_level: Number,
                 drought_level_per_hour: Number = 5, nutrient: Nutrient | None = None):
        super().__init__(start_water_level, start_nutrients_level, start_light_level, drought_level_per_hour, nutrient)


class Potato(Vegetable):
    def __init__(self, start_water_level: Number, start_nutrients_level: Number, start_light_level: Number,
                 drought_level_per_hour: Number = 5, nutrient: Nutrient | None = None):
        super().__init__(start_water_level, start_nutrients_level, start_light_level, drought_level_per_hour, nutrient)

if __name__ == '__main__':
    corn = Corn(70, 70, 80)
    print(corn)

    tomato = Tomato(10, 10, 10)
    print(tomato)

    potato = Potato(10, 10, 10)
    print(potato)

    corn_sample = Sample(corn, OPTIMAL_ENVIRONMENT_LEVELS["Corn"])
    print(corn_sample.check_sample())

