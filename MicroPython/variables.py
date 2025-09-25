import machine, pico_i2c_lcd
VERSION = "1"

I2C_ADDR = 39   # 20x4 Screen
#I2C_ADDR = 63  # 16x2 Screen
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)
lcd = pico_i2c_lcd.I2cLcd(i2c,I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

WINNING_SCORE = 0
TIMER = 300
TIMEOUT = False
playing = True

ERROR_MOD = 20

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

