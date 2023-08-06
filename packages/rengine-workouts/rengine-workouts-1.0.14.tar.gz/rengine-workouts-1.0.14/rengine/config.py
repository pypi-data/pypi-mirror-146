from rengine.dataset import get_dataset
from rengine.config_proxy import EquipmentAvailable, ExerciseName

class MuscleGroup:
    BICEPS = "Biceps"
    BACK = "Back"
    CHEST = "Chest"
    TRICEPS = "Triceps"
    CALVES = "Calves"
    HAMSTRINGS = "Hamstrings"
    QUAD = "Quads"
    DELTOIDS = "Deltoids"
    ALL = tuple(["Back", "Calves", "Chest", "Hamstrings", "Quads", "Deltoids", "Triceps", "Biceps"])
    LOWER_BODY = tuple(["Calves", "Hamstrings", "Quads"])
    UPPER_BODY = tuple(["Back", "Chest", "Deltoids", "Triceps", "Biceps"])
    PUSH = ("Chest", "Triceps", "Deltoids")
    PULL = ("Back", "Biceps")
    LEGS = ("Calves", "Hamstrings", "Quads")

class ExerciseType:
    STRENGTH = "Strength"
    HYPERTROPHY = "Hypertrophy"
    ENDURANCE = "Endurance"
    ALL = tuple(["Strength", "Hypertrophy", "Endurance"])


class ExerciseLoad:
    HEAVY = "heavy"
    MEDIUM = "medium"
    LIGHT = "light"
    ALL = tuple(["heavy", "medium", "light"])


class ExperienceLevel:
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediated"
    EXPERIENCED = "Experienced"
    ALL = tuple(["Beginner", "Intermediated", "Experienced"])

class WorkoutSplit:
    PUSH_PULL_LEGS = "ppl"
    BRO_SPLIT = "bs"
    UPPER_LOWER_SPLIT = "uls" 
    FULL_BODY = "fb"
    PHUl = "phul"
    PHAT = "phat"
    ALL = ("ppl", "bs", "uls", "fb", "phul", "phat")



EXERCISE_CATEGORY_DATA = {
    ExerciseType.STRENGTH:{
        ExerciseLoad.HEAVY: {
            "chance": 0.2,
            "sets": 5,
            "rep_range": (2,4),
            "rest_time_range": (3,5)
        },
        ExerciseLoad.MEDIUM: {
            "chance": 0.7,
            "sets": 4,
            "rep_range": (5,8),
            "rest_time_range": (2,4)
        },
        ExerciseLoad.LIGHT:{
            "chance": 0.1,
            "sets": 4,
            "rep_range": (9,10),
            "rest_time_range": (2,3)
        }
    },
    ExerciseType.HYPERTROPHY:{
        ExerciseLoad.HEAVY: {
            "chance": 0.1,
            "sets": 4,
            "rep_range": (6,7),
            "rest_time_range": (1,3)
        },
        ExerciseLoad.MEDIUM: {
            "chance": 0.8,
            "sets": 4,
            "rep_range": (8,12),
            "rest_time_range": (1,2)
        },
        ExerciseLoad.LIGHT:{
            "chance": 0.1,
            "sets": 3,
            "rep_range": (13,15),
            "rest_time_range": (1,2)
        }
    },
    ExerciseType.ENDURANCE:{
        ExerciseLoad.HEAVY: {
            "chance": 0.1,
            "sets": 4,
            "rep_range": (13,14),
            "rest_time_range": (1,2)
        },
        ExerciseLoad.MEDIUM: {
            "chance": 0.75,
            "sets": 3,
            "rep_range": (15,20),
            "rest_time_range": (1,2)
        },
        ExerciseLoad.LIGHT:{
            "chance": 0.15,
            "sets": 2,
            "rep_range": (21,30),
            "rest_time_range": (1,2)
        }
    }
}

"""
For time based conditions using following dictionary.
include_strength: Bool                  -> Whether or not auto generate should include the strength exercise
set_reductions: dict                    -> Set reductions for each exercise load in each exercise type
endurance_exercises_probabilities: list -> Each additional float in this list represents the probability the an endurance exercise is generated
caps: dict                              -> Limit the amount of exercises of a certain muscle group that can be generated based on the time of the workout
"""
TIME_BASED_CONDITIONS = {
    15: {
        "allowed_strength_loads": [],
        "set_reductions": {
            ExerciseType.HYPERTROPHY: {ExerciseLoad.HEAVY: 2, ExerciseLoad.MEDIUM: 2, ExerciseLoad.LIGHT:1}
        },
        "endurance_exercises_probabilities": [],
        "caps": {MuscleGroup.BICEPS: 1, MuscleGroup.TRICEPS:1, MuscleGroup.DELTOIDS:1, MuscleGroup.CALVES:1}
    },
    30: {
        "allowed_strength_loads": [],
        "set_reductions": {
            ExerciseType.HYPERTROPHY: {ExerciseLoad.HEAVY: 1, ExerciseLoad.MEDIUM: 1, ExerciseLoad.LIGHT:1}
        },
        "endurance_exercises_probabilities": [],
        "caps": {MuscleGroup.BICEPS: 1, MuscleGroup.TRICEPS:1, MuscleGroup.DELTOIDS:1, MuscleGroup.CALVES:1}
    },
    45: {
        "allowed_strength_loads": [ExerciseLoad.MEDIUM, ExerciseLoad.LIGHT],
        "set_reductions": {
            ExerciseType.STRENGTH: {ExerciseLoad.MEDIUM: 1, ExerciseLoad.LIGHT:1},
            ExerciseType.HYPERTROPHY: {ExerciseLoad.HEAVY: 1, ExerciseLoad.MEDIUM: 1, ExerciseLoad.LIGHT:1},
            ExerciseType.ENDURANCE: {ExerciseLoad.HEAVY: 1, ExerciseLoad.MEDIUM: 1}
        
        },
        "endurance_exercises_probabilities": [0.5],
        "caps": {MuscleGroup.BICEPS: 1, MuscleGroup.TRICEPS:1, MuscleGroup.DELTOIDS:1, MuscleGroup.CALVES:1}
    },
    60: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1],
        "caps": {MuscleGroup.BICEPS: 2, MuscleGroup.TRICEPS:2, MuscleGroup.DELTOIDS:2, MuscleGroup.CALVES:1}
    },
    75: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1],
        "caps": {MuscleGroup.BICEPS: 2, MuscleGroup.TRICEPS:2, MuscleGroup.DELTOIDS:2, MuscleGroup.CALVES:2}
    },
    90: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1],
        "caps": {MuscleGroup.BICEPS: 3, MuscleGroup.TRICEPS:3, MuscleGroup.DELTOIDS:3, MuscleGroup.CALVES:2}
    },
    105: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1,0.5],
        "caps": {MuscleGroup.BICEPS: 3, MuscleGroup.TRICEPS:3, MuscleGroup.DELTOIDS:3, MuscleGroup.CALVES:2}
    },
    120: {
        "allowed_strength_loads": ExerciseLoad.ALL,
        "set_reductions": {},
        "endurance_exercises_probabilities": [1,0.5],
        "caps": {MuscleGroup.BICEPS: 3, MuscleGroup.TRICEPS:3, MuscleGroup.DELTOIDS:3, MuscleGroup.CALVES:2}
    },
}



STRENGTH_EXERICSE_PRIORTIES = {
    MuscleGroup.HAMSTRINGS:{
        "squat":{
            "priority": 1,
            "variation_priorities":{
                "Squat Rack":"Barbell Squat",
                "Smith Machine":"Smith Machine Squat",
                "Dumbbells":"Dumbbell Squat"       #not in strength exercises
            }
        },
        "deadlift":{
            "priority": 1,
            "variation_pri orities":{
                "Romanian Deadlift": 1,
                "Sumo-Deadlift": 1,
                "Smith Machine Deadlift":2,
                "Smith Machine Sumo Deadlift":2
            }
        },
    

    

},
    "bench_press":{
        "priority": 1,
        "muscle_groups": [MuscleGroup.CHEST],
        "variation_priorities":{
            "Barbell Bench Press": 1,
            "Smith Machine Bench Press": 2,
            "Dumbell Bench Press":3   #Not in strength exercises
        }
    },
    "shoulder_press":{
        "priority": 2,
        "muscle_groups": [MuscleGroup.DELTOIDS],
        "variation_priorities":{
            "Barbell Shoulder Press": 1,
            "Smith Machine Shoulder Press": 2,   #Not in strength exercises
            "Dumbell Shoulder Press":3   #Not sure if this is the name
        }
    },
    "barbell_row":{
        "priority": 2,
        "muscle_groups": [MuscleGroup.BACK],
        "variation_priorities":{
            "Bent-Over Barbell Row",
            "Bent-Over Smith Machine Row",   #Not in strength exercises
            "Bent-Over Dumbbell Row"
        }
    },
    "pull_ups":{
        "priority": 2,
        "muscle_groups": [MuscleGroup.BACK],
        "variation_priorities":{
            "Weighted Pull-Ups":1
        }
    }
}


AUTO_GENERATED_WORKOUT_PLAN_SPLIT_CONFIG = {
    WorkoutSplit.FULL_BODY:{
        "muscles_worked_by_day":{
            1: [MuscleGroup.ALL for i in range(1)],
            2: [MuscleGroup.ALL for i in range(2)],
            3: [MuscleGroup.ALL for i in range(3)],
            4: [MuscleGroup.ALL for i in range(4)],
            5: [MuscleGroup.ALL for i in range(5)],
            6: [MuscleGroup.ALL for i in range(6)],
            7: [MuscleGroup.ALL for i in range(7)]
        }
    },
    WorkoutSplit.UPPER_LOWER_SPLIT:{
        "muscles_worked_by_day":{
            2:[MuscleGroup.UPPER_BODY, MuscleGroup.LOWER_BODY],
            4:[MuscleGroup.UPPER_BODY, MuscleGroup.LOWER_BODY, MuscleGroup.UPPER_BODY, MuscleGroup.LOWER_BODY],
            6:[MuscleGroup.UPPER_BODY, MuscleGroup.LOWER_BODY, MuscleGroup.UPPER_BODY, MuscleGroup.LOWER_BODY, MuscleGroup.UPPER_BODY, MuscleGroup.LOWER_BODY]
        }
    },
    WorkoutSplit.BRO_SPLIT:{
        "muscles_worked_by_day":{
            6:[(MuscleGroup.CHEST), (MuscleGroup.BACK), (MuscleGroup.BICEPS), (MuscleGroup.DELTOIDS), (MuscleGroup.TRICEPS), MuscleGroup.LOWER_BODY]
        }
    },
    WorkoutSplit.PUSH_PULL_LEGS:{
        "muscles_worked_by_day":{
            3:[MuscleGroup.PUSH, MuscleGroup.PULL, MuscleGroup.LEGS],
            6:[MuscleGroup.PUSH, MuscleGroup.PULL, MuscleGroup.LEGS, MuscleGroup.PUSH, MuscleGroup.PULL, MuscleGroup.LEGS]
        }
    }
} 


EXERCISE_DF = get_dataset("clean_data.csv")



ExerciseTypeValues = dict(
    Strength = 3,
    Hypertrophy = 2,
    Endurance = 1,
)
ExerciseLoadValues = dict(
    heavy = 3,
    medium = 2,
    light = 1
)