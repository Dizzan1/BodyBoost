# Copyright (C) 2026 Donovan Torres
# Licensed under the GNU Affero General Public License v3.0
# https://www.gnu.org/licenses/agpl-3.0.html

from . import config
import json
import random

# Different types of rutines
# Notice force -> all, secondarymuscles -> all

######### LEVELS #########
full_body_levels = {
    "beginner": [
        ["chest", "shoulders"],
        ["quadriceps", "hamstrings", "glutes"],
        ["middle back", "lower back"]
    ],
    "intermediate": [
        ["chest", "shoulders"],
        ["quadriceps", "hamstrings", "glutes"],
        ["middle back", "lower back"],
        ["glutes", "calves"]
    ],
    "expert": [
        ["chest", "shoulders"],
        ["quadriceps", "hamstrings", "glutes"],
        ["middle back", "lower back"],
        ["glutes", "calves"],
        ["biceps", "triceps"]
    ]
}

upper_lower_levels = [
    {
        # Upper
        "beginner": [
            ["chest", "shoulders"],
            ["biceps", "triceps"],
            ["middle back", "lower back"]
        ],
        "intermediate": [
            ["chest", "shoulders"],
            ["biceps", "triceps"],
            ["middle back", "lower back", "traps"],
            ["forearms", "neck"],
        ],
        "expert": [
            ["chest", "shoulders"],
            ["biceps", "triceps"],
            ["middle back", "lower back", "traps"],
            ["forearms", "neck"],
            ["lats", "traps"]
        ]
    },
    {
        # Lower
        "beginner": [
            ["quadriceps", "hamstrings"],
            ["glutes", "calves"],
            ["lower back", "abdominals"]
        ],
        "intermediate": [
            ["quadriceps", "hamstrings"],
            ["glutes", "calves"],
            ["lower back", "abdominals"],
            ["abductors", "adductors"]
        ],
        "expert": [
            ["quadriceps"],
            ["glutes", "calves"],
            ["lower back", "abdominals"],
            ["abductors", "adductors"],
            ["hamstrings"]
        ]
    }
]

body_part_levels = [
    {
        # Chest
        "beginner": [
            ["chest"],
            ["chest"],
            ["triceps"]
        ],
        "intermediate": [
            ["chest"],
            ["chest"],
            ["abdominals"],
            ["triceps"],
            ["triceps"]
        ],
        "expert": [
            ["chest"],
            ["chest"],
            ["chest"],
            ["abdominals"],
            ["triceps"],
            ["triceps"]
        ]
    },
    {
        # Back
        "beginner": [
            ["lower back"],
            ["middle back"],
            ["biceps"]
        ],
        "intermediate": [
            ["middle back"],
            ["lower back"],
            ["lats"],
            ["biceps"],
            ["traps"]
        ],
        "expert": [
            ["middle back"],
            ["lower back"],
            ["middle back"],
            ["lats"],
            ["biceps"],
            ["traps"]
        ]
    },
    {
        # Shoulders
        "beginner": [
            ["shoulders"],
            ["shoulders"],
            ["traps"]
        ],
        "intermediate": [
            ["shoulders"],
            ["shoulders"],
            ["shoulders"],
            ["traps"],
            ["neck"]

        ],
        "expert": [
            ["shoulders"],
            ["shoulders"],
            ["shoulders"],
            ["shoulders"],
            ["traps"],
            ["neck"]
        ]
    },
    {
        # Legs
        "beginner": [
            ["quadriceps"],
            ["hamstrings"],
            ["glutes"]
        ],
        "intermediate": [
            ["quadriceps"],
            ["abductors"],
            ["adductors"],
            ["glutes"],
            ["calves"]
        ],
        "expert": [
            ["quadriceps"],
            ["abductors"],
            ["adductors"],
            ["hamstrings"],
            ["glutes"],
            ["calves"]
        ]
    },
    {
        # Arms
        "beginner": [
            ["biceps"],
            ["biceps"],
            ["triceps"]
        ],
        "intermediate": [
            ["biceps"],
            ["biceps"],
            ["biceps"],
            ["triceps"],
            ["triceps"]
        ],
        "expert": [
            ["biceps"],
            ["biceps"],
            ["biceps"],
            ["biceps"],
            ["triceps"],
            ["forearms"]
        ]
    }
]

secondary_muscles = [
    "abdominals",
    "abductors",
    "adductors",
    "biceps",
    "calves",
    "chest",
    "forearms",
    "glutes",
    "hamstrings",
    "lats",
    "lower back",
    "middle back",
    "neck",
    "quadriceps",
    "shoulders",
    "traps",
    "triceps"
]

force_parameter = [
    None,
    "static",
    "pull",
    "push"
]

category_hypertrophy = [
    "strength"
]

category_power = [
    "powerlifting",
    "strength",
    "olympic weightlifting",
    "strongman",
    "plyometrics"
]

category_endurance = [
    "cardio",
    "strength"
]

######### ROUTINES #########
routine_parameters = {
    "full_body": {
        "hypertrophy": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["expert", "intermediate"]
            },
            "mechanic": ["compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", None],
            "primaryMuscles": [full_body_levels],
            "secondaryMuscles": secondary_muscles,
            "category": category_hypertrophy
        },
        "power": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["expert", "intermediate"]
            },
            "mechanic": ["compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", None],
            "primaryMuscles": [full_body_levels],
            "secondaryMuscles": secondary_muscles,
            "category": category_power

        },
        "endurance": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["intermediate", "beginner"]
            },
            "mechanic": ["compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", "medicine ball", "bands", "foam roll", "exercise ball", None],
            "primaryMuscles": [full_body_levels],
            "secondaryMuscles": secondary_muscles,
            "category": category_endurance
        },
    },
    "upper_lower": {

        "hypertrophy": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["expert", "intermediate"]
            },
            "mechanic": ["compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", None],
            "primaryMuscles": upper_lower_levels,
            "secondaryMuscles": secondary_muscles,
            "category": category_hypertrophy
        },
        "power": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["expert", "intermediate"]
            },
            "mechanic": ["compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", None],
            "primaryMuscles": upper_lower_levels,
            "secondaryMuscles": secondary_muscles,
            "category": category_power
        },
        "endurance": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["intermediate", "beginner"]
            },
            "mechanic": ["compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", "medicine ball", "bands", "foam roll", "exercise ball", None],
            "primaryMuscles": upper_lower_levels,
            "secondaryMuscles": secondary_muscles,
            "category": category_endurance
        }
    },
    "body_part": {
        "hypertrophy": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["expert", "intermediate"]
            },
            "mechanic": ["isolation", "compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", None],
            "primaryMuscles": body_part_levels,
            "secondaryMuscles": secondary_muscles,
            "category": category_hypertrophy
        },
        "power": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["expert", "intermediate"]
            },
            "mechanic": ["isolation", "compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", None],
            "primaryMuscles": body_part_levels,
            "secondaryMuscles": secondary_muscles,
            "category": category_power
        },
        "endurance": {
            "force": force_parameter,
            "level": {
                "beginner": ["beginner"],
                "intermediate": ["intermediate", "beginner"],
                "expert": ["intermediate", "beginner"]
            },
            "mechanic": ["isolation", "compound"],
            "equipment": ["barbell", "dumbbell", "machine", "cable", "body only", "kettlebells", "e-z curl bar", "medicine ball", "bands", "foam roll", "exercise ball", None],
            "primaryMuscles": body_part_levels,
            "secondaryMuscles": secondary_muscles,
            "category": category_endurance
        }
    }
}


# Generate routine
def generate_routine(type_routine: str, goal: str, user_level: str):

    # Check user input

    if type_routine not in ["full_body", "upper_lower", "body_part"]:
        print("Wrong spelling routine")
        return None

    if goal not in ["hypertrophy", "power", "endurance"]:
        print("Wrong spelling goal")
        return None

    if user_level not in ["beginner", "intermediate", "expert"]:
        print("Wrong spelling level -> beginner, intermediate, expert")
        return None

    # Load data exercises
    with open(config.DATA_PATH, "r") as file:
        data = json.load(file)

    keys = {
        "full_body": ["full_body_day"],
        "upper_lower": ["upper_day", "lower_day"],
        "body_part": ["chest_day", "back_day", "shoulders_day", "legs_day", "arms_day"],
    }

    routine = {}

    for counter, day_exercise in enumerate(routine_parameters[type_routine][goal]["primaryMuscles"]):

        routine[keys[type_routine][counter]] = final_ex(
            data,
            routine_parameters[type_routine][goal]["force"],
            routine_parameters[type_routine][goal]["level"][user_level],
            routine_parameters[type_routine][goal]["mechanic"],
            routine_parameters[type_routine][goal]["equipment"],
            day_exercise[user_level],
            routine_parameters[type_routine][goal]["secondaryMuscles"],
            routine_parameters[type_routine][goal]["category"]
        )

    if not routine:
        return None

    return routine


# Put together exercises
def final_ex(data, force, search_levels, mechanic, equipment, list_primaryMuscles, secondaryMuscles, category):

    final_exercises = []

    for primaryMuscles in list_primaryMuscles:
        # If one muscle
        if len(primaryMuscles) == 1:

            final_exercises.append(
                filter_and_sample(
                    data,
                    force,
                    search_levels,
                    mechanic,
                    equipment,
                    primaryMuscles[0],
                    secondaryMuscles,
                    category
                )
            )

        # If more muscles
        else:

            final_exercises.append(
                random.sample(
                    [filter_and_sample(
                        data,
                        force,
                        search_levels,
                        mechanic,
                        equipment,
                        primaryMuscle,
                        secondaryMuscles,
                        category
                    ) for primaryMuscle in primaryMuscles], 1)[0]
            )

    return final_exercises


# Filter the exercises
def filter_and_sample(data, force, search_levels, mechanic, equipment, primaryMuscle, secondaryMuscles, category):

    # Search exercise, if not found, decrease restrictions
    print("1")

    # 1
    filtered_exercises = [
        exercise for exercise in data
        if exercise["force"] in force
        and exercise["level"] in search_levels
        and exercise["mechanic"] in mechanic
        and exercise["equipment"] in equipment
        and primaryMuscle in exercise["primaryMuscles"]
        # If all elements of one list are present in another
        and (not exercise["secondaryMuscles"] or set(exercise["secondaryMuscles"]).issubset(set(secondaryMuscles)))
        and exercise["category"] in category
    ]

    if len(filtered_exercises) != 0:
        # Randomly select the desired number of exercises
        # [0] to return only the dict, not lis[dict]
        return random.sample(filtered_exercises, 1)[0]

    print("2")
    # 2
    filtered_exercises = [
        exercise for exercise in data
        if exercise["level"] in search_levels
        and exercise["mechanic"] in mechanic
        and exercise["equipment"] in equipment
        and primaryMuscle in exercise["primaryMuscles"]
        and exercise["category"] in category
    ]

    if len(filtered_exercises) != 0:
        return random.sample(filtered_exercises, 1)[0]

    print("3")
    # 3
    filtered_exercises = [
        exercise for exercise in data
        if exercise["level"] in search_levels
        and exercise["mechanic"] in mechanic
        and primaryMuscle in exercise["primaryMuscles"]
        and exercise["category"] in category
    ]

    if len(filtered_exercises) != 0:
        return random.sample(filtered_exercises, 1)[0]

    print("4")
    # 4
    filtered_exercises = [
        exercise for exercise in data
        if exercise["level"] in search_levels
        and exercise["mechanic"] in mechanic
        and primaryMuscle in exercise["secondaryMuscles"]
        and exercise["category"] in category
    ]

    print("5")
    # 5
    filtered_exercises = [
        exercise for exercise in data
        if exercise["level"] in search_levels
        and exercise["mechanic"] in mechanic
        and exercise["category"] in category
    ]

    if len(filtered_exercises) != 0:
        return random.sample(filtered_exercises, 1)[0]

    print("6")
    # 6
    filtered_exercises = [
        exercise for exercise in data
        if exercise["level"] in search_levels
        and exercise["category"] in category
    ]

    if len(filtered_exercises) != 0:
        return random.sample(filtered_exercises, 1)[0]

    print("7")
    # 7
    filtered_exercises = [
        exercise for exercise in data
        if exercise["category"] in category
    ]

    if len(filtered_exercises) != 0:
        return random.sample(filtered_exercises, 1)[0]

    print("No excercise found")
    return None
