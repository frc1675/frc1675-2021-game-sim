import json
import numpy
import math


def read_json_data(json_file):
    # Reads data from json file into an ordered dictionary in python
    with open(json_file, "r") as test_dict:
        test_dict = json.load(test_dict)
    return test_dict


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
    global painting_score_value
    global statue_score_value
    global paintings_scored
    global statues_scored

    robot_score = 0

    if robot_task_end == time_left:
        if robot_task == "Low Painting" or robot_task == "Mid Painting" or robot_task == "High Painting":
            robot_score = painting_score_value
            paintings_scored += 1
        elif robot_task == "Near Statue" or robot_task == "Far Statue":
            robot_score = statue_score_value
            statues_scored += 1

    if time_left == auto_length + teleop_length or robot_task_end == time_left:
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
        print("%s Task: %s - Time (%r)" % (robot, robot_task, math.ceil(robot_execution["Task Cycle"])))
    return robot_score, robot_task, robot_task_end


def generate_match_data():

    robot_dict = read_json_data("Robots.json")

    # Create randomizer to select robot types

    red1 = "Red 1"
    red1_type = "God Bot"
    red1_task = ""
    red1_task_end = 0
    red1_total_score = 0

    red2 = "Red 2"
    red2_type = "God Bot"
    red2_task = ""
    red2_task_end = 0
    red2_total_score = 0

    red3 = "Red 3"
    red3_type = "God Bot"
    red3_task = ""
    red3_task_end = 0
    red3_total_score = 0

    blue1 = "Blue 1"
    blue1_type = "God Bot"
    blue1_task = ""
    blue1_task_end = 0
    blue1_total_score = 0

    blue2 = "Blue 2"
    blue2_type = "God Bot"
    blue2_task = ""
    blue2_task_end = 0
    blue2_total_score = 0

    blue3 = "Blue 3"
    blue3_type = "God Bot"
    blue3_task = ""
    blue3_task_end = 0
    blue3_total_score = 0

    for time_left in range(auto_length + teleop_length, 0, -1):
        red1_increment_score, red1_task, red1_task_end = robot_match_increment(robot_dict, red1, red1_type, red1_task,
                                                                               red1_task_end, time_left)
        red1_total_score += red1_increment_score

        red2_increment_score, red2_task, red2_task_end = robot_match_increment(robot_dict, red2, red2_type, red2_task,
                                                                               red2_task_end, time_left)
        red2_total_score += red2_increment_score

        red3_increment_score, red3_task, red3_task_end = robot_match_increment(robot_dict, red3, red3_type, red3_task,
                                                                               red3_task_end, time_left)
        red3_total_score += red3_increment_score
        
        blue1_increment_score, blue1_task, blue1_task_end = robot_match_increment(robot_dict, blue1, blue1_type,
                                                                                  blue1_task, blue1_task_end, time_left)
        blue1_total_score += blue1_increment_score

        blue2_increment_score, blue2_task, blue2_task_end = robot_match_increment(robot_dict, blue2, blue2_type,
                                                                                  blue2_task, blue2_task_end, time_left)
        blue2_total_score += blue2_increment_score

        blue3_increment_score, blue3_task, blue3_task_end = robot_match_increment(robot_dict, blue3, blue3_type,
                                                                                  blue3_task, blue3_task_end, time_left)
        blue3_total_score += blue3_increment_score

    print("Red 1 Score: %d" % red1_total_score)
    print("Red 2 Score: %d" % red2_total_score)
    print("Red 3 Score: %d" % red3_total_score)
    print("Blue 1 Score: %d" % blue1_total_score)
    print("Blue 2 Score: %d" % blue2_total_score)
    print("Blue 3 Score: %d" % blue3_total_score)
    print("Paintings Scored: %d" % paintings_scored)
    print("Statues Scored: %d" % statues_scored)


auto_length = 15
teleop_length = 135
red_near_statues = 2
red_far_statues = 2
blue_near_statues = 2
blue_far_statues = 2
low_paintings = 24
mid_paintings = 8
high_paintings = 24
painting_score_value = 10
statue_score_value = 15
statues_scored = 0
paintings_scored = 0

generate_match_data()
