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
    "ELITE": {
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


def add_robot_to_dict(dictionary, strategy, quality):
    robot_type = quality + " " + strategy
    print(robot_type)
    dictionary.update(
        {
            robot_type: {
                "Low Painting": {
                    "Auto Priority": ROBOT_STRATEGY[strategy]["Low Painting"]["Auto Priority"],
                    "TeleOp Priority": ROBOT_STRATEGY[strategy]["Low Painting"]["TeleOp Priority"],
                    "Endgame Priority": ROBOT_STRATEGY[strategy]["Low Painting"]["Endgame Priority"],
                    "Cycle": ROBOT_QUALITY[quality]["Low Painting"]["Cycle"],
                    "Cycle_StdDev": ROBOT_QUALITY[quality]["Low Painting"]["Cycle_StdDev"],
                    "Auto Reliability": ROBOT_QUALITY[quality]["Low Painting"]["Auto Reliability"],
                    "Reliability": ROBOT_QUALITY[quality]["Low Painting"]["Reliability"]
                },
                "Mid Painting": {
                    "Auto Priority": ROBOT_STRATEGY[strategy]["Mid Painting"]["Auto Priority"],
                    "TeleOp Priority": ROBOT_STRATEGY[strategy]["Mid Painting"]["TeleOp Priority"],
                    "Endgame Priority": ROBOT_STRATEGY[strategy]["Mid Painting"]["Endgame Priority"],
                    "Cycle": ROBOT_QUALITY[quality]["Mid Painting"]["Cycle"],
                    "Cycle_StdDev": ROBOT_QUALITY[quality]["Mid Painting"]["Cycle_StdDev"],
                    "Auto Reliability": ROBOT_QUALITY[quality]["Mid Painting"]["Auto Reliability"],
                    "Reliability": ROBOT_QUALITY[quality]["Mid Painting"]["Reliability"]
                },
                "High Painting": {
                    "Auto Priority": ROBOT_STRATEGY[strategy]["High Painting"]["Auto Priority"],
                    "TeleOp Priority": ROBOT_STRATEGY[strategy]["High Painting"]["TeleOp Priority"],
                    "Endgame Priority": ROBOT_STRATEGY[strategy]["High Painting"]["Endgame Priority"],
                    "Cycle": ROBOT_QUALITY[quality]["High Painting"]["Cycle"],
                    "Cycle_StdDev": ROBOT_QUALITY[quality]["High Painting"]["Cycle_StdDev"],
                    "Auto Reliability": ROBOT_QUALITY[quality]["High Painting"]["Auto Reliability"],
                    "Reliability": ROBOT_QUALITY[quality]["High Painting"]["Reliability"]
                },
                "Floor Painting": {
                    "TeleOp Priority": ROBOT_STRATEGY[strategy]["Floor Painting"]["TeleOp Priority"],
                    "Endgame Priority": ROBOT_STRATEGY[strategy]["Floor Painting"]["Endgame Priority"],
                    "Cycle": ROBOT_QUALITY[quality]["Floor Painting"]["Cycle"],
                    "Cycle_StdDev": ROBOT_QUALITY[quality]["Floor Painting"]["Cycle_StdDev"],
                    "Reliability": ROBOT_QUALITY[quality]["Floor Painting"]["Reliability"]
                },
                "Near Statue": {
                    "Auto Priority": ROBOT_STRATEGY[strategy]["Near Statue"]["Auto Priority"],
                    "TeleOp Priority": ROBOT_STRATEGY[strategy]["Near Statue"]["Auto Priority"],
                    "Cycle": ROBOT_QUALITY[quality]["Near Statue"]["Cycle"],
                    "Cycle_StdDev": ROBOT_QUALITY[quality]["Near Statue"]["Cycle_StdDev"],
                    "Auto Reliability": ROBOT_QUALITY[quality]["Near Statue"]["Auto Reliability"],
                    "Reliability": ROBOT_QUALITY[quality]["Near Statue"]["Reliability"]
                },
                "Far Statue": {
                    "TeleOp Priority": ROBOT_STRATEGY[strategy]["Far Statue"]["Auto Priority"],
                    "Cycle": ROBOT_QUALITY[quality]["Far Statue"]["Cycle"],
                    "Cycle_StdDev": ROBOT_QUALITY[quality]["Far Statue"]["Cycle_StdDev"],
                    "Reliability": ROBOT_QUALITY[quality]["Far Statue"]["Reliability"]
                },
                "Fire System": {
                    "TeleOp Priority": ROBOT_STRATEGY[strategy]["Fire System"]["TeleOp Priority"],
                    "Endgame Priority": ROBOT_STRATEGY[strategy]["Fire System"]["Endgame Priority"],
                    "Cycle": ROBOT_QUALITY[quality]["Fire System"]["Cycle"],
                    "Cycle_StdDev": ROBOT_QUALITY[quality]["Fire System"]["Cycle_StdDev"],
                    "Reliability": ROBOT_QUALITY[quality]["Fire System"]["Reliability"]
                },
                "Chain Pull": {
                    "Endgame Priority": ROBOT_STRATEGY[strategy]["Chain Pull"]["Endgame Priority"],
                    "Cycle": ROBOT_QUALITY[quality]["Chain Pull"]["Cycle"],
                    "Cycle_StdDev": ROBOT_QUALITY[quality]["Chain Pull"]["Cycle_StdDev"],
                    "Reliability": ROBOT_QUALITY[quality]["Chain Pull"]["Reliability"],
                }
            }
        }
    )
    print(dictionary)



print("====================================================")
print("Selection a robot strategy from the following list: ")
for strategy_key in ROBOT_STRATEGY.keys():
    print(strategy_key)
print("====================================================")
strategy_selection = input("Enter Robot Strategy Selection: ").upper()

print("====================================================")
print("Selection a robot quality from the following list: ")
for quality_key in ROBOT_QUALITY.keys():
    print(quality_key)
print("====================================================")
quality_selection = input("Enter Robot Quality Selection: ").upper()

robot_dict = {}

add_robot_to_dict(robot_dict, strategy_selection, quality_selection)
