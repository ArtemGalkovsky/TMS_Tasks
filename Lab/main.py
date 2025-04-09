from config_vegetables import OPTIMAL_ENVIRONMENT_LEVELS
from subclasses import Corn, Tomato, Potato, CustomizableLamp
from main_classes import Assistant, Sample, VegetableDiedException
from minor_classes import Timer, Nutrient
from main_config import (WORKING_DAY_LENGTH, DAY_LENGTH_HOURS, TEST_DAYS, INITIAL_LAMP_BREAK_CHANCE_MAX,
                         START_NUTRIENT_STRENGTH, START_NUTRIENT_REDUCTION_MULTIPLIER, START_NUTRIENT_REDUCTION_LEVEL)
from random import seed, randrange

NOT_WORKING_HOURS_NUMBER = DAY_LENGTH_HOURS - WORKING_DAY_LENGTH

input_seed = input("Enter seed if you want (must be 4+ symbols length) or shorten than 4 symbols length to generate random seed > ")
if len(input_seed) < 4:
    input_seed = f"{randrange(1000000)}"

seed(input_seed)


timer = Timer(8)

assistant = Assistant("John", "Junior")

sample = Sample(Corn(70, 65, 2), OPTIMAL_ENVIRONMENT_LEVELS["Corn"],
                (
                    CustomizableLamp(30, INITIAL_LAMP_BREAK_CHANCE_MAX),
                    CustomizableLamp(50, INITIAL_LAMP_BREAK_CHANCE_MAX)
                )
)

assistant.focus_on_object(sample)

timer.connect_update_function(sample.update_sample_stats)

nutrient = Nutrient(START_NUTRIENT_STRENGTH, START_NUTRIENT_REDUCTION_LEVEL, START_NUTRIENT_REDUCTION_MULTIPLIER)
sample.add_nutrients(nutrient)

timer.update()

day_passed = 0
try:
    for day_number in range(1, TEST_DAYS+1):
        print("-" * 100)
        print("New working day just started!")

        for hour in range(WORKING_DAY_LENGTH):
            timer.add_hours()

            print(f"Day {day_number}: Working hour {hour + 1} starts. Sample stats:", assistant.get_object_info())

            assistant.request_action()



        for hour in range(NOT_WORKING_HOURS_NUMBER):
            timer.add_hours()

            print(f"Day {day_number}: Chill hour {hour + 1} ends. Sample stats:", assistant.get_object_info())

        day_passed += 1

    print(f"{assistant} IS THE GREATEST WORKER! EXAM PASSED! SEED:", input_seed)
except VegetableDiedException as e:
    print(f"{assistant} ruined the test! GG WP! Bye bye! SEED: {input_seed}\n")
    print("DEATH REPORT:")
    print(e)

