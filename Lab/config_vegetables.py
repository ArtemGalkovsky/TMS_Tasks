from dataclasses import dataclass

@dataclass(frozen=True)
class OptimalEnvironmentLevels:
    water_level_min: float
    water_level_max: float

    nutrients_level_min: float
    nutrients_level_max: float

    light_level_min: float
    light_level_max: float


CORN_OPTIMAL_ENVIRONMENT_LEVELS = OptimalEnvironmentLevels(
    water_level_min=60,
    water_level_max=80,

    nutrients_level_min=60,
    nutrients_level_max=70,

    light_level_min=75,
    light_level_max=85,
)

TOMATO_OPTIMAL_ENVIRONMENT_LEVELS = OptimalEnvironmentLevels(
    water_level_min=50,
    water_level_max=70,

    nutrients_level_min=60,
    nutrients_level_max=80,

    light_level_min=70,
    light_level_max=85,
)

POTATO_OPTIMAL_ENVIRONMENT_LEVELS = OptimalEnvironmentLevels(
    water_level_min=50,
    water_level_max=60,

    nutrients_level_min=45,
    nutrients_level_max=55,

    light_level_min=60,
    light_level_max=70,
)

OPTIMAL_ENVIRONMENT_LEVELS: dict[str, OptimalEnvironmentLevels] = {
    "Corn": CORN_OPTIMAL_ENVIRONMENT_LEVELS,
    "Tomato": TOMATO_OPTIMAL_ENVIRONMENT_LEVELS,
    "Potato": POTATO_OPTIMAL_ENVIRONMENT_LEVELS,
}


__all__ = ["OPTIMAL_ENVIRONMENT_LEVELS", "OptimalEnvironmentLevels"]