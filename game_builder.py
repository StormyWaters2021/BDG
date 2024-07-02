import random
from variables import *

LED_PATTERNS = {
    0: {
        "sequence": [RED_LED, GREEN_LED, BLUE_LED, ],
        "solves": [BLUE_BUTTON, GREEN_TOGGLE, ORANGE_ROCKER, ],
        "exclude": [GREEN_BUTTON, BLUE_TOGGLE],
        },
    1: {
        "sequence": [RED_LED, BLUE_LED, GREEN_LED, ],
        "solves": [BLUE_BUTTON, WHITE_BUTTON, ORANGE_ROCKER, ],
        "exclude": [GREEN_BUTTON, YELLOW_BUTTON],
        },
    2: {
        "sequence": [BLUE_LED, RED_LED, GREEN_LED, ],
        "solves": [RED_TOGGLE, WHITE_BUTTON, ORANGE_ROCKER, ],
        "exclude": [RED_BUTTON, ORANGE_TOGGLE],
        },
    3: {
        "sequence": [BLUE_LED, GREEN_LED, RED_LED, ],
        "solves": [RED_TOGGLE, BLACK_WIRE, ORANGE_ROCKER, ],
        "exclude": [ORANGE_TOGGLE, BLUE_TOGGLE],
        },    
    4: {
        "sequence": [GREEN_LED, BLUE_LED, RED_LED, ],
        "solves": [YELLOW_WIRE, BLACK_WIRE, ORANGE_ROCKER, ],
        "exclude": [YELLOW_BUTTON, GREEN_ROCKER],
        },    
    5: {
        "sequence": [GREEN_LED, RED_LED, BLUE_LED, ],
        "solves": [YELLOW_WIRE, GREEN_TOGGLE, ORANGE_ROCKER, ],
        "exclude": [RED_BUTTON, GREEN_ROCKER],
        },    
    6: {
        "sequence": [RED_LED, GREEN_LED, RED_LED, ],
        "solves": [RED_TOGGLE, GREEN_TOGGLE, RED_ROCKER],
        "exclude": [GREEN_BUTTON, BLUE_TOGGLE],
        },    
    7: {
        "sequence": [RED_LED, BLUE_LED, RED_LED, ],
        "solves": [YELLOW_WIRE, WHITE_BUTTON, RED_ROCKER, ],
        "exclude": [GREEN_BUTTON, YELLOW_BUTTON],
        },    
    8: {
        "sequence": [GREEN_LED, RED_LED, GREEN_LED, ],
        "solves": [RED_TOGGLE, GREEN_TOGGLE, RED_ROCKER, ],
        "exclude": [RED_BUTTON, GREEN_ROCKER],
        },    
    9: {
        "sequence": [GREEN_LED, BLUE_LED, GREEN_LED, ],
        "solves": [BLUE_BUTTON, BLACK_WIRE, RED_ROCKER, ],
        "exclude": [YELLOW_BUTTON, GREEN_ROCKER],
        },    
    10: {
        "sequence": [BLUE_LED, GREEN_LED, BLUE_LED, ],
        "solves": [BLUE_BUTTON, BLACK_WIRE, RED_ROCKER, ],
        "exclude": [ORANGE_TOGGLE, BLUE_TOGGLE],
        },    
    11: {
        "sequence": [BLUE_LED, RED_LED, BLUE_LED, ],
        "solves": [YELLOW_WIRE, WHITE_BUTTON, RED_ROCKER, ],
        "exclude": [RED_BUTTON, ORANGE_TOGGLE],
        },          
}

SERIAL_SOLUTIONS = [RED_BUTTON, GREEN_BUTTON, YELLOW_BUTTON, ORANGE_TOGGLE, BLUE_TOGGLE, WHITE_TOGGLE, GREEN_ROCKER, BLUE_ROCKER, RED_WIRE, GREEN_WIRE, BLUE_WIRE]

SERIAL_CODE = {
    RED_WIRE: (["C", "E", "G", "I"], 1),
    ORANGE_TOGGLE: (["1", "2", "6", ], 2),
    YELLOW_BUTTON: (["L", "M", "J", "K", ], 3),
    GREEN_WIRE: (["1", "3", "5", "7", ], 4),
    BLUE_ROCKER: (["2", "4", "6", "8"], 5),
    BLUE_TOGGLE: (["A", "E", "I", "U", ], 6),
    GREEN_BUTTON: (["N", "P", "Q", "R", ], 7),
    BLUE_WIRE: (["1", "8", ], 8),
    GREEN_ROCKER: (["1", "2", "3", ], 9),
    WHITE_TOGGLE: (["S", "P", ], 10),
    RED_BUTTON: (["C", "I", "E", ], 11),
}


def game_selector():
    global game

    solutions = random.randint(8, 10)                               # Number of "correct" answers needed

    led_slot = random.randint(0, 11) # Select one random pattern of LED flashes
    game["led_seq"] = LED_PATTERNS[led_slot]["sequence"]            # Store the light sequence 
    game["winners_on"].extend(LED_PATTERNS[led_slot]["solves"])    # Store the solutions guaranteed by the LED sequence

    extra_pulls = [i for i in SERIAL_SOLUTIONS if i not in LED_PATTERNS[led_slot]["exclude"]]
    solutions -= len(game["winners_on"])

    for _ in range(solutions):
        extra = random.choice(extra_pulls)
        game["winners_on"].append(extra)
        extra_pulls.remove(extra)

    for item in game["winners_on"]:
        if item in SERIAL_CODE.keys():
            game["serial"] = game["serial"][:SERIAL_CODE[item][1]] + random.choice(SERIAL_CODE[item][0]) + game["serial"][SERIAL_CODE[item][1] + 1:]

    for item in LED_PATTERNS[led_slot]["exclude"]:
        if item in SERIAL_CODE.keys():
            game["serial"] = game["serial"][:SERIAL_CODE[item][1]] + random.choice(SERIAL_CODE[item][0]) + game["serial"][SERIAL_CODE[item][1] + 1:]

    return game
