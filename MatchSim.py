import json
import numpy
import math
from Constants import *


def percent_limit(percentage):
    if percentage > 100:
        percentage = 100
    elif percentage < 0:
        percentage = 0
    return percentage


def generate_robot_data(robot_dict, robot_type, robot_task):
    task_cycle_key = robot_dict[robot_type][robot_task]["Cycle"]
    task_cycle_sd_key = robot_dict[robot_type][robot_task]["Cycle_StdDev"]
    task_reliability = robot_dict[robot_type][robot_task]["Reliability"]
    task_cycle_time = numpy.random.normal(task_cycle_key, task_cycle_sd_key)

    robot_execution = {
        "Current Task": robot_task,
        "Task Cycle": task_cycle_time,
        "Task Reliability": task_reliability
    }

    return robot_execution


def task_selection(robot_dict, robot, robot_type):
    teleop_priority = {
        "Low Painting": robot_dict[robot_type]["Low Painting"]["Priority"],
        "Mid Painting": robot_dict[robot_type]["Mid Painting"]["Priority"],
        "High Painting": robot_dict[robot_type]["High Painting"]["Priority"],
        "Near Statue": robot_dict[robot_type]["Near Statue"]["Priority"],
        "Far Statue": robot_dict[robot_type]["Far Statue"]["Priority"],
    }
    endgame_priority = {
        "Low Painting": robot_dict[robot_type]["Low Painting"]["Priority"],
        "Mid Painting": robot_dict[robot_type]["Mid Painting"]["Priority"],
        "High Painting": robot_dict[robot_type]["High Painting"]["Priority"],
        "Near Statue": robot_dict[robot_type]["Near Statue"]["Priority"],
        "Far Statue": robot_dict[robot_type]["Far Statue"]["Priority"],
        "Chain Pull": robot_dict[robot_type]["Chain Pull"]["Priority"]
    }
    if low_paintings == 0:
        teleop_priority.pop("Low Painting")
        endgame_priority.pop("Low Painting")
    if mid_paintings == 0:
        teleop_priority.pop("Mid Painting")
        endgame_priority.pop("Mid Painting")
    if high_paintings == 0:
        teleop_priority.pop("High Painting")
        endgame_priority.pop("High Painting")
    if red_near_statues == 0 and robot.startswith("R"):
        teleop_priority.pop("Near Statue")
        endgame_priority.pop("Near Statue")
    if blue_near_statues == 0 and robot.startswith("B"):
        teleop_priority.pop("Near Statue")
        endgame_priority.pop("Near Statue")
    if red_far_statues == 0 and robot.startswith("R"):
        teleop_priority.pop("Far Statue")
        endgame_priority.pop("Far Statue")
    if blue_far_statues == 0 and robot.startswith("B"):
        teleop_priority.pop("Far Statue")
        endgame_priority.pop("Far Statue")
    task = min(teleop_priority, key=endgame_priority.get)
    return task


def robot_match_increment(robot_dict, robot, robot_type, robot_task, robot_task_end, time_left):
    global low_paintings
    global mid_paintings
    global high_paintings
    global red_near_statues
    global red_far_statues
    global blue_near_statues
    global blue_far_statues
    global paintings_scored
    global statues_scored

    robot_score = 0

    if robot_task_end == time_left:
        if robot_task == "Low Painting" or robot_task == "Mid Painting" or robot_task == "High Painting":
            robot_score = PAINTING_SCORE_VALUE
            paintings_scored += 1
        elif robot_task == "Near Statue" or robot_task == "Far Statue":
            robot_score = STATUE_SCORE_VALUE
            statues_scored += 1

    if time_left == AUTO_LENGTH + TELEOP_LENGTH or robot_task_end == time_left:
        robot_task = task_selection(robot_dict, robot, robot_type)
        robot_execution = generate_robot_data(robot_dict, robot_type, robot_task)
        robot_task_end = time_left - math.ceil(robot_execution["Task Cycle"])

        if robot_task == "Low Painting":
            low_paintings -= 1
        elif robot_task == "Mid Painting":
            mid_paintings -= 1
        elif robot_task == "High Painting":
            high_paintings -= 1
        elif robot_task == "Near Statue":
            if robot.startswith("R"):
                red_near_statues -= 1
            elif robot.startswith("B"):
                blue_near_statues -= 1
        elif robot_task == "Far Statue":
            if robot.startswith("R"):
                red_far_statues -= 1
            elif robot.startswith("B"):
                blue_far_statues -= 1
        # Won't print out a thousand lines when calculating average
        if sim_type == "s":
            print("%s Task: %s - Time (%r)" % (robot, robot_task, math.ceil(robot_execution["Task Cycle"])))
    return robot_score, robot_task, robot_task_end


def generate_match_data(r1, r2, r3, b1, b2, b3):
    # Create the six robots
    red1 = "Red 1"
    red1_type = r1
    red1_task = ""
    red1_task_end = 0
    red1_total_score = 0

    red2 = "Red 2"
    red2_type = r2
    red2_task = ""
    red2_task_end = 0
    red2_total_score = 0

    red3 = "Red 3"
    red3_type = r3
    red3_task = ""
    red3_task_end = 0
    red3_total_score = 0

    blue1 = "Blue 1"
    blue1_type = b1
    blue1_task = ""
    blue1_task_end = 0
    blue1_total_score = 0

    blue2 = "Blue 2"
    blue2_type = b2
    blue2_task = ""
    blue2_task_end = 0
    blue2_total_score = 0

    blue3 = "Blue 3"
    blue3_type = b3
    blue3_task = ""
    blue3_task_end = 0
    blue3_total_score = 0

    # Reset the field
    global red_near_statues
    global red_far_statues
    global blue_near_statues
    global blue_far_statues
    global low_paintings
    global mid_paintings
    global high_paintings
    global statues_scored 
    global paintings_scored

    red_near_statues = 2
    red_far_statues = 2
    blue_near_statues = 2
    blue_far_statues = 2
    low_paintings = 24
    mid_paintings = 8
    high_paintings = 24
    statues_scored = 0
    paintings_scored = 0

    for time_left in range(AUTO_LENGTH + TELEOP_LENGTH, 0, -1):
        red1_increment_score, red1_task, red1_task_end = \
            robot_match_increment(ROBOT_DICT, red1, red1_type, red1_task, red1_task_end, time_left)
        red1_total_score += red1_increment_score

        red2_increment_score, red2_task, red2_task_end = \
            robot_match_increment(ROBOT_DICT, red2, red2_type, red2_task, red2_task_end, time_left)
        red2_total_score += red2_increment_score

        red3_increment_score, red3_task, red3_task_end = \
            robot_match_increment(ROBOT_DICT, red3, red3_type, red3_task, red3_task_end, time_left)
        red3_total_score += red3_increment_score
        
        blue1_increment_score, blue1_task, blue1_task_end = \
            robot_match_increment(ROBOT_DICT, blue1, blue1_type, blue1_task, blue1_task_end, time_left)
        blue1_total_score += blue1_increment_score

        blue2_increment_score, blue2_task, blue2_task_end = \
            robot_match_increment(ROBOT_DICT, blue2, blue2_type, blue2_task, blue2_task_end, time_left)
        blue2_total_score += blue2_increment_score

        blue3_increment_score, blue3_task, blue3_task_end = \
            robot_match_increment(ROBOT_DICT, blue3, blue3_type, blue3_task, blue3_task_end, time_left)
        blue3_total_score += blue3_increment_score

    # Results at the end of match
    red_total_score = red1_total_score + red2_total_score + red3_total_score
    blue_total_score = blue1_total_score + blue2_total_score + blue3_total_score
    if red_total_score > blue_total_score:
        win_message = RED_WIN_MESSAGE
    elif blue_total_score > red_total_score:
        win_message = BLUE_WIN_MESSAGE
    else:
        win_message = TIE_WIN_MESSAGE

    # Won't print out a thousand lines when calculating average
    if sim_type == "s":
        print("=====================")
        print("=======RESULTS=======")
        print("=====================")
        print("Red 1 Score: %d" % red1_total_score)
        print("Red 2 Score: %d" % red2_total_score)
        print("Red 3 Score: %d" % red3_total_score)
        print("======================")
        print("Blue 1 Score: %d" % blue1_total_score)
        print("Blue 2 Score: %d" % blue2_total_score)
        print("Blue 3 Score: %d" % blue3_total_score)
        print("======================")
        print("Paintings Scored: %d" % paintings_scored)
        print("Statues Scored: %d" % statues_scored)
        print("======================")
        print("Final score: R %d -- B %d" % (red_total_score, blue_total_score))
        print(win_message)
    # Tracks total points and wins
    elif sim_type == "a":
        global blue_all_wins
        global red_all_wins
        global all_ties

        global red1_all_score
        global red2_all_score
        global red3_all_score
        global blue1_all_score
        global blue2_all_score
        global blue3_all_score

        if win_message == BLUE_WIN_MESSAGE:
            blue_all_wins += 1
        elif win_message == RED_WIN_MESSAGE:
            red_all_wins += 1
        else:
            all_ties += 1
        red1_all_score += red1_total_score
        red2_all_score += red2_total_score
        red3_all_score += red3_total_score
        blue1_all_score += blue1_total_score
        blue2_all_score += blue2_total_score
        blue3_all_score += blue3_total_score

'''============================PROGRAM STARTS HERE================================'''

red_near_statues = 2
red_far_statues = 2
blue_near_statues = 2
blue_far_statues = 2
low_paintings = 24
mid_paintings = 8
high_paintings = 24

print("Robot types: ", end="")
for type in ROBOT_DICT.keys():
    print(type, end=", ")
print("or [R]andom")

r1_type = input("Red 1 type: ").upper()
r2_type = input("Red 2 type: ").upper()
r3_type = input("Red 3 type: ").upper()
b1_type = input("Blue 1 type: ").upper()
b2_type = input("Blue 2 type: ").upper()
b3_type = input("Blue 3 type: ").upper()

sim_type = input("[S]ingle simulation or calculate [A]verage scores ").casefold()
# Single: detailed description of one simulated game
# Average: runs 1,000 games with the same robots, calculates
# average scores and win rates
if sim_type == "s":
    generate_match_data(r1_type, r2_type, r3_type, b1_type, b2_type, b3_type)
elif sim_type == "a":
    red_all_wins = 0
    blue_all_wins = 0
    all_ties = 0

    red1_all_score = 0
    red2_all_score = 0
    red3_all_score = 0
    blue1_all_score = 0
    blue2_all_score = 0
    blue3_all_score = 0

    for i in range(SIM_REPS):
        generate_match_data(r1_type, r2_type, r3_type, b1_type, b2_type, b3_type)
    
    print("=====================")
    print("=======RESULTS=======")
    print("=====================")
    print("Red win rate: %f" % (red_all_wins/SIM_REPS))
    print("Blue win rate: %f" % (blue_all_wins/SIM_REPS))
    print("=====================")
    print("Red 1 average points: %f" %(red1_all_score/SIM_REPS))
    print("Red 2 average points: %f" %(red2_all_score/SIM_REPS))
    print("Red 3 average points: %f" %(red3_all_score/SIM_REPS))
    print("Blue 1 average points: %f" %(blue1_all_score/SIM_REPS))
    print("Blue 2 average points: %f" %(blue2_all_score/SIM_REPS))
    print("Blue 3 average points: %f" %(blue3_all_score/SIM_REPS))