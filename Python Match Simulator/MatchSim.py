import numpy
import math
import random

from Constants import *


def check_reliability(robot_dict, robot_type, robot_task):
    reliability_roll = random.randint(0, 100)
    task_reliability = robot_dict[robot_type][robot_task]["Reliability"]
    if reliability_roll < task_reliability:
        task_success = True
    else:
        task_success = False
        if sim_type == "s":
            print("Task Failed: %s" % robot_task)
    return task_success


def generate_robot_data(robot_dict, robot_type, robot_task):

    task_cycle_key = robot_dict[robot_type][robot_task]["Cycle"]
    task_cycle_sd_key = robot_dict[robot_type][robot_task]["Cycle_StdDev"]
    task_cycle_time = numpy.random.normal(task_cycle_key, task_cycle_sd_key)
    task_cycle_time = math.ceil(task_cycle_time)

    return task_cycle_time


def task_selection(robot_dict, robot, robot_type, time_left):
    auto_priority = {
        "Low Painting": robot_dict[robot_type]["Low Painting"]["Auto Priority"],
        "Mid Painting": robot_dict[robot_type]["Mid Painting"]["Auto Priority"],
        "High Painting": robot_dict[robot_type]["High Painting"]["Auto Priority"],
        "Near Statue": robot_dict[robot_type]["Near Statue"]["Auto Priority"]
    }
    teleop_priority = {
        "Low Painting": robot_dict[robot_type]["Low Painting"]["TeleOp Priority"],
        "Mid Painting": robot_dict[robot_type]["Mid Painting"]["TeleOp Priority"],
        "High Painting": robot_dict[robot_type]["High Painting"]["TeleOp Priority"],
        "Floor Painting": robot_dict[robot_type]["Floor Painting"]["TeleOp Priority"],
        "Near Statue": robot_dict[robot_type]["Near Statue"]["TeleOp Priority"],
        "Far Statue": robot_dict[robot_type]["Far Statue"]["TeleOp Priority"]
    }
    endgame_priority = {
        "Low Painting": robot_dict[robot_type]["Low Painting"]["Endgame Priority"],
        "Mid Painting": robot_dict[robot_type]["Mid Painting"]["Endgame Priority"],
        "High Painting": robot_dict[robot_type]["High Painting"]["Endgame Priority"],
        "Floor Painting": robot_dict[robot_type]["High Painting"]["Endgame Priority"],
        "Chain Pull": robot_dict[robot_type]["Chain Pull"]["Endgame Priority"]
    }
    if low_paintings == 0:
        auto_priority.pop("Low Painting")
        teleop_priority.pop("Low Painting")
        endgame_priority.pop("Low Painting")
    if mid_paintings == 0:
        auto_priority.pop("Mid Painting")
        teleop_priority.pop("Mid Painting")
        endgame_priority.pop("Mid Painting")
    if high_paintings == 0:
        auto_priority.pop("High Painting")
        teleop_priority.pop("High Painting")
        endgame_priority.pop("High Painting")
    if floor_paintings == 0:
        teleop_priority.pop("Floor Painting")
        endgame_priority.pop("Floor Painting")
    if red_near_statues == 0 and robot.startswith("R"):
        auto_priority.pop("Near Statue")
        teleop_priority.pop("Near Statue")
    if blue_near_statues == 0 and robot.startswith("B"):
        auto_priority.pop("Near Statue")
        teleop_priority.pop("Near Statue")
    if red_far_statues == 0 and robot.startswith("R"):
        teleop_priority.pop("Far Statue")
    if blue_far_statues == 0 and robot.startswith("B"):
        teleop_priority.pop("Far Statue")
    if red_chain_pull == 0 and robot.startswith("R"):
        endgame_priority.pop("Chain Pull")
    if blue_chain_pull == 0 and robot.startswith("B"):
        endgame_priority.pop("Chain Pull")

    if time_left > TELEOP_LENGTH:
        task = min(auto_priority, key=auto_priority.get)
    elif time_left <= ENDGAME_LENGTH:
        task = min(endgame_priority, key=endgame_priority.get)
    else:
        task = min(teleop_priority, key=teleop_priority.get)
    return task


def robot_match_increment(robot_dict, robot, robot_type, robot_task, robot_task_end, time_left):
    global low_paintings
    global mid_paintings
    global high_paintings
    global floor_paintings
    global red_near_statues
    global red_far_statues
    global blue_near_statues
    global blue_far_statues
    global blue_chain_pull
    global red_chain_pull

    global auto_paintings_scored
    global teleop_paintings_scored
    global auto_statues_scored
    global teleop_statues_scored

    robot_score = 0

    if robot_task_end == time_left:
        task_success = check_reliability(robot_dict, robot_type, robot_task)
        if robot_task == "Low Painting" or robot_task == "Mid Painting" or robot_task == "High Painting":
            if task_success:
                if time_left > TELEOP_LENGTH:
                    robot_score = AUTO_PAINTING_SCORE_VALUE
                    auto_paintings_scored += 1
                else:
                    robot_score = PAINTING_SCORE_VALUE
                    teleop_paintings_scored += 1
            elif not task_success:
                floor_paintings += 1
        elif robot_task == "Near Statue" or robot_task == "Far Statue":
            if task_success:
                if time_left > TELEOP_LENGTH:
                    robot_score = AUTO_STATUE_SCORE_VALUE
                    auto_statues_scored += 1
                else:
                    robot_score = STATUE_SCORE_VALUE
                    teleop_statues_scored += 1
            elif not task_success:
                robot_task_end -= math.ceil(numpy.random.normal(5, 0.8))
        elif robot_task == "Chain Pull":
            if task_success:
                robot_score = CHAIN_PULL_SCORE_VALUE
            elif not task_success:
                if robot.startswith("R"):
                    red_chain_pull += 1
                elif robot.startswith("B"):
                    blue_chain_pull += 1

    if time_left == AUTO_LENGTH + TELEOP_LENGTH or robot_task_end == time_left:
        if robot_task == "Chain Pull" and task_success:
            robot_task = None
            task_cycle_time = 0
        else:
            robot_task = task_selection(robot_dict, robot, robot_type, time_left)
            task_cycle_time = generate_robot_data(robot_dict, robot_type, robot_task)
            robot_task_end = time_left - task_cycle_time

            if robot_task == "Low Painting":
                low_paintings -= 1
            elif robot_task == "Mid Painting":
                mid_paintings -= 1
            elif robot_task == "High Painting":
                high_paintings -= 1
            elif robot_task == "Floor Painting":
                floor_paintings -= 1
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
            elif robot_task == "Chain Pull":
                if robot.startswith("R"):
                    red_chain_pull -= 1
                elif robot.startswith("B"):
                    blue_chain_pull -= 1
                
        if sim_type == "s":     # Won't print out ten thousand lines when calculating average
            print("%s Task: %s - Time (%r)" % (robot, robot_task, task_cycle_time))
    return robot_score, robot_task, robot_task_end


def generate_match_data(r1, r2, r3, b1, b2, b3):
    # Select random robots
    if r1 == "R":
        r1 = random.choice(list(ROBOT_DICT.keys()))
    if r2 == "R":
        r2 = random.choice(list(ROBOT_DICT.keys()))
    if r3 == "R":
        r3 = random.choice(list(ROBOT_DICT.keys()))
    if b1 == "R":
        b1 = random.choice(list(ROBOT_DICT.keys()))
    if b2 == "R":
        b2 = random.choice(list(ROBOT_DICT.keys()))
    if b3 == "R":
        b3 = random.choice(list(ROBOT_DICT.keys()))

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

    if sim_type == "s":
        print(red1_type+", "+red2_type+", "+red3_type+" versus "+blue1_type+", "+blue2_type+", "+blue3_type)

    # Reset the field
    global low_paintings
    global mid_paintings
    global high_paintings
    global floor_paintings
    global red_near_statues
    global red_far_statues
    global blue_near_statues
    global blue_far_statues
    global red_chain_pull
    global blue_chain_pull
    global auto_paintings_scored
    global teleop_paintings_scored
    global auto_statues_scored
    global teleop_statues_scored

    red_near_statues = 2
    red_far_statues = 2
    blue_near_statues = 2
    blue_far_statues = 2
    red_chain_pull = 1
    blue_chain_pull = 1
    low_paintings = 24
    mid_paintings = 8
    high_paintings = 24
    floor_paintings = 0

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

    if sim_type == "s":     # Won't print out ten thousand lines when calculating average
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
        print("Auto Paintings Scored: %d" % auto_paintings_scored)
        print("TeleOp Paintings Scored: %d" % teleop_paintings_scored)
        print("Auto Statues Scored: %d" % auto_statues_scored)
        print("TeleOp Statues Scored: %d" % teleop_statues_scored)
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
red_chain_pull = 1
blue_chain_pull = 1
low_paintings = 24
mid_paintings = 8
high_paintings = 24
floor_paintings = 0

auto_statues_scored = 0
teleop_statues_scored = 0
auto_paintings_scored = 0
teleop_paintings_scored = 0


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
# Average: runs 10,000 games with the same robots, calculates
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
    print("Tie rate: %f" % (all_ties/SIM_REPS))
    print("=====================")
    print("Red 1 average points: %f" %(red1_all_score/SIM_REPS))
    print("Red 2 average points: %f" %(red2_all_score/SIM_REPS))
    print("Red 3 average points: %f" %(red3_all_score/SIM_REPS))
    print("Blue 1 average points: %f" %(blue1_all_score/SIM_REPS))
    print("Blue 2 average points: %f" %(blue2_all_score/SIM_REPS))
    print("Blue 3 average points: %f" %(blue3_all_score/SIM_REPS))
