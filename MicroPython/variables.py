import machine
VERSION = "1"

WINNING_SCORE = 0
TIMER = 300
TIMEOUT = False
playing = True

ERROR_MOD = 10

game = {
        "winners_on": [],
        "led_seq": [],
        "serial": "8F3N69KM74XY"
    }

BUTTONS = [28, 27, 26, 22, 21, ]
TOGGLES = [20, 19, 18, 17, 16, ]
ROCKERS = [15, 14, 13, 12, ]
WIRES = [11, 10, 9, 8, 7]

combined = [BUTTONS, TOGGLES, ROCKERS]
SWITCHES = [item for sublist in combined for item in sublist]

RED_LED = machine.Pin(2, machine.Pin.OUT)
GREEN_LED = machine.Pin(3, machine.Pin.OUT)
BLUE_LED = machine.Pin(4, machine.Pin.OUT)

RED_BUTTON = 28
GREEN_BUTTON = 27
YELLOW_BUTTON = 26
BLUE_BUTTON = 22
WHITE_BUTTON = 21

RED_TOGGLE = 20
GREEN_TOGGLE = 19
ORANGE_TOGGLE = 18
BLUE_TOGGLE = 17
WHITE_TOGGLE = 16

RED_ROCKER = 15
GREEN_ROCKER = 14
BLUE_ROCKER = 13
ORANGE_ROCKER = 12

YELLOW_WIRE = 11
RED_WIRE = 10
GREEN_WIRE = 9
BLUE_WIRE = 8
BLACK_WIRE = 7
