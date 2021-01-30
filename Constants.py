BLUE_WIN_MESSAGE = "Blue wins!"
RED_WIN_MESSAGE = "Red wins!"
TIE_WIN_MESSAGE = "It's a tie!"

SIM_REPS = 10000

AUTO_LENGTH = 15
TELEOP_LENGTH = 135

PAINTING_SCORE_VALUE = 10
STATUE_SCORE_VALUE = 15

ROBOT_DICT = {
  "GOD BOT" : {
    "Low Painting" : {
      "Cycle" : 12,
      "Cycle_StdDev" : 1.2,
      "Reliability": 97,
      "Priority": 4
    },
     "Mid Painting" : {
       "Cycle" : 14,
       "Cycle_StdDev" : 1.4,
       "Reliability": 95,
       "Priority": 5
    },
     "High Painting" : {
       "Cycle" : 16,
       "Cycle_StdDev" : 1.6,
       "Reliability": 93,
       "Priority": 6
    },
    "Near Statue" : {
      "Cycle": 15,
      "Cycle_StdDev": 3,
      "Reliability": 95,
      "Priority": 2
    },
    "Far Statue" : {
      "Cycle": 25,
      "Cycle_StdDev": 5,
      "Reliability": 93,
      "Priority": 3
    },
    "Fire System": {
      "Cycle": 3,
      "Cycle_StdDev": 0.4,
      "Reliability": 98
    },
    "Chain Pull": {
      "Cycle": 8,
      "Cycle_StdDev": 1.3,
      "Reliability": 85,
      "Priority": 1
    }
  },

  "OK BOT" : {
    "Low Painting" : {
      "Cycle" : 15,
      "Cycle_StdDev" : 1.2,
      "Reliability": 90,
      "Priority": 4
    },
     "Mid Painting" : {
       "Cycle" : 17,
       "Cycle_StdDev" : 1.4,
       "Reliability": 80,
       "Priority": 5
    },
     "High Painting" : {
       "Cycle" : 19,
       "Cycle_StdDev" : 1.6,
       "Reliability": 50,
       "Priority": 6
    },
    "Near Statue" : {
      "Cycle": 20,
      "Cycle_StdDev": 3,
      "Reliability": 90,
      "Priority": 2
    },
    "Far Statue" : {
      "Cycle": 30,
      "Cycle_StdDev": 5,
      "Reliability": 85,
      "Priority": 3
    },
    "Fire System": {
      "Cycle": 3,
      "Cycle_StdDev": 0.4,
      "Reliability": 95
    },
    "Chain Pull": {
      "Cycle": 12,
      "Cycle_StdDev": 1.3,
      "Reliability": 85,
      "Priority": 1
    }
  }
}