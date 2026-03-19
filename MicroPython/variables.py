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

RED_LED = machine.Pin(2, machine.Pin.OUT)
GREEN_LED = machine.Pin(3, machine.Pin.OUT)
BLUE_LED = machine.Pin(4, machine.Pin.OUT)

WHITE_BUTTON = 6
BLUE_BUTTON = 7
YELLOW_BUTTON = 8
GREEN_BUTTON = 9
RED_BUTTON = 10

ORANGE_ROCKER = 12
BLUE_ROCKER = 13
GREEN_ROCKER = 14
RED_ROCKER = 15

RED_TOGGLE = 16
GREEN_TOGGLE = 17
ORANGE_TOGGLE = 18
BLUE_TOGGLE = 19
WHITE_TOGGLE = 20

YELLOW_WIRE = 22
GREEN_WIRE = 26
BLUE_WIRE = 27
BLACK_WIRE = 28

BUTTONS = [RED_BUTTON, GREEN_BUTTON, YELLOW_BUTTON, BLUE_BUTTON, WHITE_BUTTON, ]
TOGGLES = [RED_TOGGLE, GREEN_TOGGLE, ORANGE_TOGGLE, BLUE_TOGGLE, WHITE_TOGGLE, ]
ROCKERS = [RED_ROCKER, GREEN_ROCKER, BLUE_ROCKER, ORANGE_ROCKER, ]
WIRES = [YELLOW_WIRE, GREEN_WIRE, BLUE_WIRE, BLACK_WIRE]

combined = [BUTTONS, TOGGLES, ROCKERS]
SWITCHES = [item for sublist in combined for item in sublist]