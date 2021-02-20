BLUE_WIN_MESSAGE = "Blue wins!"
RED_WIN_MESSAGE = "Red wins!"
TIE_WIN_MESSAGE = "It's a tie!"

SIM_REPS = 10000

AUTO_LENGTH = 15
TELEOP_LENGTH = 135
ENDGAME_LENGTH = 30

AUTO_PAINTING_SCORE_VALUE = 20
PAINTING_SCORE_VALUE = 10
AUTO_STATUE_SCORE_VALUE = 30
STATUE_SCORE_VALUE = 15
CHAIN_PULL_SCORE_VALUE = 20
CHAIN_PULL_STATUE_ADDER = 10
SPRINKLER_BUTTON_VALUE = 3

RP_STATUES_REQUIRED = 4
FIRE_ALARM_RP = 1
STATUE_LIFT_RP = 1
TIE_RP = 1
WIN_RP = 2

ALARM_1_PERIOD = 35
ALARM_2_PERIOD = 40
ALARM_3_PERIOD = 45
DEADZONE = 5
ALARM_TIME = 10

NEAR_STATUES = 2
FAR_STATUES = 2
LOW_PAINTINGS = 16
MID_PAINTINGS = 24
HIGH_PAINTINGS = 32
FLOOR_PAINTINGS = 0
CHAIN_PULL = 2

ROBOT_STRATEGY = {
    "ALL BOT": {
        "Low Painting": {
            "Auto Priority": 3,
            "TeleOp Priority": 4,
            "Endgame Priority": 3
        },
        "Mid Painting": {
            "Auto Priority": 2,
            "TeleOp Priority": 5,
            "Endgame Priority": 4
        },
        "High Painting": {
            "Auto Priority": 4,
            "TeleOp Priority": 7,
            "Endgame Priority": 6
        },
        "Floor Painting": {
            "TeleOp Priority": 6,
            "Endgame Priority": 5
        },
        "Near Statue": {
            "Auto Priority": 1,
            "TeleOp Priority": 1
        },
        "Far Statue": {
            "TeleOp Priority": 3
        },
        "Fire System": {
            "TeleOp Priority": 2,
            "Endgame Priority": 2
        },
        "Chain Pull": {
            "Endgame Priority": 1
        }
    }
}

ROBOT_QUALITY = {
    "BEST": {
        "Low Painting": {
            "Cycle": 12,
            "Cycle_StdDev": 1.2,
            "Auto Reliability": 90,
            "Reliability": 97
        },
        "Mid Painting": {
            "Cycle": 14,
            "Cycle_StdDev": 1.4,
            "Auto Reliability": 94,
            "Reliability": 95
        },
        "High Painting": {
            "Cycle": 16,
            "Cycle_StdDev": 1.6,
            "Auto Reliability": 90,
            "Reliability": 93
        },
        "Floor Painting": {
            "Cycle": 12,
            "Cycle_StdDev": 2.2,
            "Reliability": 97
        },
        "Near Statue": {
            "Cycle": 15,
            "Cycle_StdDev": 3,
            "Auto Reliability": 92,
            "Reliability": 95
        },
        "Far Statue": {
            "Cycle": 25,
            "Cycle_StdDev": 5,
            "Reliability": 95
        },
        "Fire System": {
            "Cycle": 3,
            "Cycle_StdDev": 0.4,
            "Reliability": 98
        },
        "Chain Pull": {
            "Cycle": 8,
            "Cycle_StdDev": 1.3,
            "Reliability": 92
        }
    }
}
