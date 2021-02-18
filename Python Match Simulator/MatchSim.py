import numpy
import math
import random

from Constants import *


def fire_alarms_initialize():
    # generates random times within the 3 set alarm periods when the alarms will turn
    # randomly picks which alarms will be active during each period

    # alarm cycle 1: 135-100s left in match (1 Alarm)
    # alarm cycle 2: 99-60s left in match (2 Alarms)
    # alarm cycle 3: 59-15s left in match (1 Alarm)
    global alarm_config
    global red_alarms_active
    global blue_alarms_active
    global red_alarm_end
    global blue_alarm_end
    global red_period1_alarm_fail
    global red_period2_alarm_fail
    global red_period3_alarm_fail
    global blue_period1_alarm_fail
    global blue_period2_alarm_fail
    global blue_period3_alarm_fail
    global red_period1_alarm_set
    global red_period2_alarm_set
    global red_period3_alarm_set
    global blue_period1_alarm_set
    global blue_period2_alarm_set
    global blue_period3_alarm_set

    red_alarms_active = []
    blue_alarms_active = []
    red_alarm_end = 0
    blue_alarm_end = 0

    red_period1_alarm_fail = False
    red_period2_alarm_fail = False
    red_period3_alarm_fail = False
    blue_period1_alarm_fail = False
    blue_period2_alarm_fail = False
    blue_period3_alarm_fail = False

    red_period1_alarm_set = False
    red_period2_alarm_set = False
    red_period3_alarm_set = False
    blue_period1_alarm_set = False
    blue_period2_alarm_set = False
    blue_period3_alarm_set = False

    alarm_period1_end = TELEOP_LENGTH - ALARM_1_PERIOD
    alarm_period2_end = TELEOP_LENGTH - ALARM_1_PERIOD - ALARM_2_PERIOD
    alarm_period3_end = TELEOP_LENGTH - ALARM_1_PERIOD - ALARM_2_PERIOD - ALARM_3_PERIOD

    red_period1_alarm_start = numpy.random.randint(alarm_period1_end + DEADZONE, TELEOP_LENGTH+1)
    red_period1_active_alarms = list(numpy.random.choice(range(1, 4), 1, replace=False))

    red_period2_alarm_start = numpy.random.randint(alarm_period2_end + DEADZONE, alarm_period1_end - DEADZONE)
    red_period2_active_alarms = list(numpy.random.choice(range(1, 4), 2, replace=False))

    red_period3_alarm_start = numpy.random.randint(alarm_period3_end + DEADZONE, alarm_period2_end - DEADZONE)
    red_period3_active_alarms = list(numpy.random.choice(range(1, 4), 1, replace=False))

    blue_period1_alarm_start = numpy.random.randint(alarm_period1_end + DEADZONE, TELEOP_LENGTH+1)
    blue_period1_active_alarms = list(numpy.random.choice(range(1, 4), 1, replace=False))

    blue_period2_alarm_start = numpy.random.randint(alarm_period2_end + DEADZONE, alarm_period1_end - DEADZONE)
    blue_period2_active_alarms = list(numpy.random.choice(range(1, 4), 2, replace=False))

    blue_period3_alarm_start = numpy.random.randint(alarm_period3_end + DEADZONE, alarm_period2_end - DEADZONE)
    blue_period3_active_alarms = list(numpy.random.choice(range(1, 4), 1, replace=False))

    alarm_config = {
        "Red": {
            "Period 1": {
                "Alarm Start": red_period1_alarm_start,
                "Alarms Active": red_period1_active_alarms
            },
            "Period 2": {
                "Alarm Start": red_period2_alarm_start,
                "Alarms Active": red_period2_active_alarms
            },
            "Period 3": {
                "Alarm Start": red_period3_alarm_start,
                "Alarms Active": red_period3_active_alarms
            }
        },
        "Blue": {
            "Period 1": {
                "Alarm Start": blue_period1_alarm_start,
                "Alarms Active": blue_period1_active_alarms
            },
            "Period 2": {
                "Alarm Start": blue_period2_alarm_start,
                "Alarms Active": blue_period2_active_alarms
            },
            "Period 3": {
                "Alarm Start": blue_period3_alarm_start,
                "Alarms Active": blue_period3_active_alarms
            }
        }
    }


def check_alarms(robot, time_left):

    global red_alarms_active
    global red_alarm_end
    global blue_alarms_active
    global blue_alarm_end
    global red_period1_alarm_fail
    global red_period2_alarm_fail
    global red_period3_alarm_fail
    global blue_period1_alarm_fail
    global blue_period2_alarm_fail
    global blue_period3_alarm_fail
    global red_period1_alarm_set
    global red_period2_alarm_set
    global red_period3_alarm_set
    global blue_period1_alarm_set
    global blue_period2_alarm_set
    global blue_period3_alarm_set

    alliance = ""

    if robot.startswith("R"):
        alliance = "Red"
    elif robot.startswith("B"):
        alliance = "Blue"
    period1_alarm_start = alarm_config[alliance]["Period 1"]["Alarm Start"]
    period2_alarm_start = alarm_config[alliance]["Period 2"]["Alarm Start"]
    period3_alarm_start = alarm_config[alliance]["Period 3"]["Alarm Start"]

    if len(red_alarms_active) == 0 and alliance == "Red":
        if period2_alarm_start < time_left <= period1_alarm_start and not red_period1_alarm_set:
            red_period1_alarm_set = True
            red_alarms_active = alarm_config[alliance]["Period 1"]["Alarms Active"]
            red_alarm_end = time_left - ALARM_TIME
            if sim_type == "s":
                print("Period 1 - Red Alarm", red_alarms_active, red_alarm_end)
        elif period3_alarm_start < time_left <= period2_alarm_start and not red_period2_alarm_set:
            red_period2_alarm_set = True
            red_alarms_active = alarm_config[alliance]["Period 2"]["Alarms Active"]
            red_alarm_end = time_left - ALARM_TIME
            if sim_type == "s":
                print("Period 2 - Red Alarm", red_alarms_active, red_alarm_end)
        elif time_left <= period3_alarm_start and not red_period3_alarm_set:
            red_period3_alarm_set = True
            red_alarms_active = alarm_config[alliance]["Period 3"]["Alarms Active"]
            red_alarm_end = time_left - ALARM_TIME
            if sim_type == "s":
                print("Period 3 - Red Alarm", red_alarms_active, red_alarm_end)
    if time_left == red_alarm_end and alliance == "Red" and len(red_alarms_active) != 0:
        red_alarms_active = []
        if time_left == period1_alarm_start - ALARM_TIME:
            red_period1_alarm_fail = True
            if sim_type == "s":
                print("~~~Red Period 1 Alarm - FAIL~~~")
        elif time_left == period2_alarm_start - ALARM_TIME:
            red_period2_alarm_fail = True
            if sim_type == "s":
                print("~~~Red Period 2 Alarm - FAIL~~~")
        elif time_left == period3_alarm_start - ALARM_TIME:
            red_period3_alarm_fail = True
            if sim_type == "s":
                print("~~~Red Period 3 Alarm - FAIL~~~")

    if len(blue_alarms_active) == 0 and alliance == "Blue":
        if period2_alarm_start < time_left <= period1_alarm_start and not blue_period1_alarm_set:
            blue_period1_alarm_set = True
            blue_alarms_active = alarm_config[alliance]["Period 1"]["Alarms Active"]
            blue_alarm_end = time_left - ALARM_TIME
            if sim_type == "s":
                print("Period 1 - Blue Alarm", blue_alarms_active, blue_alarm_end)
        elif period3_alarm_start < time_left <= period2_alarm_start and not blue_period2_alarm_set:
            blue_period2_alarm_set = True
            blue_alarms_active = alarm_config[alliance]["Period 2"]["Alarms Active"]
            blue_alarm_end = time_left - ALARM_TIME
            if sim_type == "s":
                print("Period 2 - Blue Alarm", blue_alarms_active, blue_alarm_end)
        elif time_left <= period3_alarm_start and not blue_period3_alarm_set:
            blue_period3_alarm_set = True
            blue_alarms_active = alarm_config[alliance]["Period 3"]["Alarms Active"]
            blue_alarm_end = time_left - ALARM_TIME
            if sim_type == "s":
                print("Period 3 - Blue Alarm", blue_alarms_active, blue_alarm_end)
    if time_left == blue_alarm_end and alliance == "Blue" and len(blue_alarms_active) != 0:
        blue_alarms_active = []
        if time_left == period1_alarm_start - ALARM_TIME:
            blue_period1_alarm_fail = True
            if sim_type == "s":
                print("~~~Blue Period 1 Alarm - FAIL~~~")
        elif time_left == period2_alarm_start - ALARM_TIME:
            blue_period2_alarm_fail = True
            if sim_type == "s":
                print("~~~Blue Period 2 Alarm - FAIL~~~")
        elif time_left == period3_alarm_start - ALARM_TIME:
            blue_period3_alarm_fail = True
            if sim_type == "s":
                print("~~~Blue Period 3 Alarm - FAIL~~~")


def check_reliability(robot_type, robot_task):
    task_success = False
    reliability_roll = numpy.random.randint(0, 100+1)
    if robot_task is not None:
        task_reliability = ROBOT_DICT[robot_type][robot_task]["Reliability"]
        if reliability_roll < task_reliability:
            task_success = True
        else:
            task_success = False
            if sim_type == "s":
                print("Task Failed: %s" % robot_task)
    return task_success


def generate_robot_data(robot_type, robot_task):

    task_cycle_key = ROBOT_DICT[robot_type][robot_task]["Cycle"]
    task_cycle_sd_key = ROBOT_DICT[robot_type][robot_task]["Cycle_StdDev"]
    task_cycle_time = numpy.random.normal(task_cycle_key, task_cycle_sd_key)
    task_cycle_time = math.ceil(task_cycle_time)

    return task_cycle_time


def decrement_game_object_stock(robot, robot_task):
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


def task_selection(robot, robot_type, time_left):
    auto_priority = {
        "Low Painting": ROBOT_DICT[robot_type]["Low Painting"]["Auto Priority"],
        "Mid Painting": ROBOT_DICT[robot_type]["Mid Painting"]["Auto Priority"],
        "High Painting": ROBOT_DICT[robot_type]["High Painting"]["Auto Priority"],
        "Near Statue": ROBOT_DICT[robot_type]["Near Statue"]["Auto Priority"]
    }
    teleop_priority = {
        "Low Painting": ROBOT_DICT[robot_type]["Low Painting"]["TeleOp Priority"],
        "Mid Painting": ROBOT_DICT[robot_type]["Mid Painting"]["TeleOp Priority"],
        "High Painting": ROBOT_DICT[robot_type]["High Painting"]["TeleOp Priority"],
        "Floor Painting": ROBOT_DICT[robot_type]["Floor Painting"]["TeleOp Priority"],
        "Near Statue": ROBOT_DICT[robot_type]["Near Statue"]["TeleOp Priority"],
        "Far Statue": ROBOT_DICT[robot_type]["Far Statue"]["TeleOp Priority"]
    }
    endgame_priority = {
        "Low Painting": ROBOT_DICT[robot_type]["Low Painting"]["Endgame Priority"],
        "Mid Painting": ROBOT_DICT[robot_type]["Mid Painting"]["Endgame Priority"],
        "High Painting": ROBOT_DICT[robot_type]["High Painting"]["Endgame Priority"],
        "Floor Painting": ROBOT_DICT[robot_type]["High Painting"]["Endgame Priority"],
        "Chain Pull": ROBOT_DICT[robot_type]["Chain Pull"]["Endgame Priority"]
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


def robot_match_increment(robot, robot_type, robot_task, robot_task_end, alarm_task_end, time_left):
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
    global red_auto_paintings_scored
    global blue_auto_paintings_scored

    global teleop_paintings_scored
    global red_teleop_paintings_scored
    global blue_teleop_paintings_scored

    global auto_statues_scored
    global red_auto_statues_scored
    global blue_auto_statues_scored

    global teleop_statues_scored
    global red_teleop_statues_scored
    global blue_teleop_statues_scored

    robot_score = 0
    current_task_priority = 0
    fire_system_priority = 0

    check_alarms(robot, time_left)
    if time_left == AUTO_LENGTH + TELEOP_LENGTH:
        robot_task = task_selection(robot, robot_type, time_left)
        task_cycle_time = generate_robot_data(robot_type, robot_task)
        robot_task_end = time_left - task_cycle_time
        decrement_game_object_stock(robot, robot_task)

# check if hitting a sprinkler button is a higher priority than the current task
    if time_left > ENDGAME_LENGTH:
        fire_system_priority = ROBOT_DICT[robot_type]["Fire System"]["TeleOp Priority"]
        current_task_priority = ROBOT_DICT[robot_type][robot_task]["TeleOp Priority"]
    elif time_left <= ENDGAME_LENGTH and robot_task is not None:
        fire_system_priority = ROBOT_DICT[robot_type]["Fire System"]["Endgame Priority"]
        current_task_priority = ROBOT_DICT[robot_type][robot_task]["Endgame Priority"]

# give a robot the fire alarm task, while there are fire alarm tasks remaining
    if robot.startswith("R") and len(red_alarms_active) > 0 and fire_system_priority <= current_task_priority:
        red_alarms_active.pop()
        alarm_task_time = generate_robot_data(robot_type, "Fire System")
        alarm_task_end = time_left - alarm_task_time
        robot_task_end -= alarm_task_time
        if sim_type == "s":
            print("--- Red Alarm Task Started: %s - Time (%s)" % (robot, alarm_task_time))
    elif robot.startswith("B") and len(blue_alarms_active) > 0 and fire_system_priority <= current_task_priority:
        blue_alarms_active.pop()
        alarm_task_time = generate_robot_data(robot_type, "Fire System")
        alarm_task_end = time_left - alarm_task_time
        robot_task_end -= alarm_task_time
        if sim_type == "s":
            print("--- Blue Alarm Task Started: %s - Time (%s)" % (robot, alarm_task_time))

# score successful alarm task
    if alarm_task_end == time_left:
        alarm_success = check_reliability(robot_type, "Fire System")
        if alarm_success:
            robot_score = SPRINKLER_BUTTON_VALUE
        elif not alarm_success:
            if robot.startswith("R"):
                red_alarms_active.append(1)
            elif robot.startswith("B"):
                blue_alarms_active.append(1)

# when robot completes a non-alarm task, add appropriate score and select new task
    if robot_task_end == time_left:
        task_success = check_reliability(robot_type, robot_task)
        if robot_task == "Low Painting" or robot_task == "Mid Painting" or robot_task == "High Painting":
            if task_success:
                if time_left > TELEOP_LENGTH:
                    robot_score = AUTO_PAINTING_SCORE_VALUE
                    if robot.startswith("R"):
                        red_auto_paintings_scored += 1
                    elif robot.startswith("B"):
                        blue_auto_paintings_scored += 1
                else:
                    robot_score = PAINTING_SCORE_VALUE
                    if robot.startswith("R"):
                        red_auto_paintings_scored += 1
                    elif robot.startswith("B"):
                        blue_auto_paintings_scored += 1
            elif not task_success:
                floor_paintings += 1
        elif robot_task == "Near Statue" or robot_task == "Far Statue":
            if task_success:
                if time_left > TELEOP_LENGTH:
                    robot_score = AUTO_STATUE_SCORE_VALUE
                    if robot.startswith("R"):
                        red_auto_statues_scored += 1
                    elif robot.startswith("B"):
                        blue_auto_statues_scored += 1
                else:
                    robot_score = STATUE_SCORE_VALUE
                    if robot.startswith("R"):
                        red_teleop_statues_scored += 1
                    elif robot.startswith("B"):
                        blue_teleop_statues_scored += 1
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

        if robot_task == "Chain Pull" and task_success:
            robot_task = None
            task_cycle_time = 0
        else:
            robot_task = task_selection(robot, robot_type, time_left)
            task_cycle_time = generate_robot_data(robot_type, robot_task)
            robot_task_end = time_left - task_cycle_time
            decrement_game_object_stock(robot, robot_task)

        if sim_type == "s":     # Won't print out ten thousand lines when calculating average
            print("%s Task: %s - Time (%r)" % (robot, robot_task, task_cycle_time))
    return robot_score, robot_task, robot_task_end, alarm_task_end


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
    red1_alarm_task_end = 0

    red2 = "Red 2"
    red2_type = r2
    red2_task = ""
    red2_task_end = 0
    red2_total_score = 0
    red2_alarm_task_end = 0

    red3 = "Red 3"
    red3_type = r3
    red3_task = ""
    red3_task_end = 0
    red3_total_score = 0
    red3_alarm_task_end = 0

    blue1 = "Blue 1"
    blue1_type = b1
    blue1_task = ""
    blue1_task_end = 0
    blue1_total_score = 0
    blue1_alarm_task_end = 0

    blue2 = "Blue 2"
    blue2_type = b2
    blue2_task = ""
    blue2_task_end = 0
    blue2_total_score = 0
    blue2_alarm_task_end = 0

    blue3 = "Blue 3"
    blue3_type = b3
    blue3_task = ""
    blue3_task_end = 0
    blue3_total_score = 0
    blue3_alarm_task_end = 0

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

    red_near_statues = NEAR_STATUES
    red_far_statues = FAR_STATUES
    blue_near_statues = NEAR_STATUES
    blue_far_statues = FAR_STATUES
    red_chain_pull = CHAIN_PULL
    blue_chain_pull = CHAIN_PULL
    low_paintings = LOW_PAINTINGS
    mid_paintings = MID_PAINTINGS
    high_paintings = HIGH_PAINTINGS
    floor_paintings = FLOOR_PAINTINGS

    fire_alarms_initialize()

    for time_left in range(AUTO_LENGTH + TELEOP_LENGTH, 0, -1):
        red1_increment_score, red1_task, red1_task_end, red1_alarm_task_end = \
            robot_match_increment(red1, red1_type, red1_task, red1_task_end, red1_alarm_task_end,  time_left)
        red1_total_score += red1_increment_score

        red2_increment_score, red2_task, red2_task_end, red2_alarm_task_end = \
            robot_match_increment(red2, red2_type, red2_task, red2_task_end, red2_alarm_task_end, time_left)
        red2_total_score += red2_increment_score

        red3_increment_score, red3_task, red3_task_end, red3_alarm_task_end = \
            robot_match_increment(red3, red3_type, red3_task, red3_task_end, red3_alarm_task_end, time_left)
        red3_total_score += red3_increment_score
        
        blue1_increment_score, blue1_task, blue1_task_end, blue1_alarm_task_end = \
            robot_match_increment(blue1, blue1_type, blue1_task, blue1_task_end, blue1_alarm_task_end, time_left)
        blue1_total_score += blue1_increment_score

        blue2_increment_score, blue2_task, blue2_task_end, blue2_alarm_task_end = \
            robot_match_increment(blue2, blue2_type, blue2_task, blue2_task_end, blue2_alarm_task_end, time_left)
        blue2_total_score += blue2_increment_score

        blue3_increment_score, blue3_task, blue3_task_end, blue3_alarm_task_end = \
            robot_match_increment(blue3, blue3_type, blue3_task, blue3_task_end, blue3_alarm_task_end, time_left)
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
        print("Red Auto Paintings Scored: %d" % red_auto_paintings_scored)
        print("Red TeleOp Paintings Scored: %d" % red_teleop_paintings_scored)
        print("Red Auto Statues Scored: %d" % red_auto_statues_scored)
        print("Red TeleOp Statues Scored: %d" % red_teleop_statues_scored)
        print("======================")
        print("Blue 1 Score: %d" % blue1_total_score)
        print("Blue 2 Score: %d" % blue2_total_score)
        print("Blue 3 Score: %d" % blue3_total_score)
        print("Blue Auto Paintings Scored: %d" % blue_auto_paintings_scored)
        print("Blue TeleOp Paintings Scored: %d" % blue_teleop_paintings_scored)
        print("Blue Auto Statues Scored: %d" % blue_auto_statues_scored)
        print("Blue TeleOp Statues Scored: %d" % blue_teleop_statues_scored)
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

red_near_statues = NEAR_STATUES
red_far_statues = FAR_STATUES
blue_near_statues = NEAR_STATUES
blue_far_statues = FAR_STATUES
red_chain_pull = CHAIN_PULL
blue_chain_pull = CHAIN_PULL
low_paintings = LOW_PAINTINGS
mid_paintings = MID_PAINTINGS
high_paintings = HIGH_PAINTINGS
floor_paintings = FLOOR_PAINTINGS

red_alarms_active = []
blue_alarms_active = []
red_alarm_end = 0
blue_alarm_end = 0

red_period1_alarm_fail = False
red_period2_alarm_fail = False
red_period3_alarm_fail = False
blue_period1_alarm_fail = False
blue_period2_alarm_fail = False
blue_period3_alarm_fail = False

red_period1_alarm_set = False
red_period2_alarm_set = False
red_period3_alarm_set = False
blue_period1_alarm_set = False
blue_period2_alarm_set = False
blue_period3_alarm_set = False

alarm_config = {}

auto_statues_scored = 0
red_auto_statues_scored = 0
blue_auto_statues_scored = 0
teleop_statues_scored = 0
red_teleop_statues_scored = 0
blue_teleop_statues_scored = 0
auto_paintings_scored = 0
red_auto_paintings_scored = 0
blue_auto_paintings_scored = 0
teleop_paintings_scored = 0
red_teleop_paintings_scored = 0
blue_teleop_paintings_scored = 0


print("Robot types: ", end="")
for r_type in ROBOT_DICT.keys():
    print(r_type, end=", ")
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
    print("Red 1 average points: %f" % (red1_all_score/SIM_REPS))
    print("Red 2 average points: %f" % (red2_all_score/SIM_REPS))
    print("Red 3 average points: %f" % (red3_all_score/SIM_REPS))
    print("Blue 1 average points: %f" % (blue1_all_score/SIM_REPS))
    print("Blue 2 average points: %f" % (blue2_all_score/SIM_REPS))
    print("Blue 3 average points: %f" % (blue3_all_score/SIM_REPS))
