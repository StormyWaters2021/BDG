import machine, pico_i2c_lcd, _thread
INTRO_LINES = [
    "   Cipher Solver   ",
    "    Escape Games    ",
    "      Presents      ",
    "   TICK TOCK BOOM   "
]

WAITING_LINES = [
    "  Waiting for game  ",
    "    to be reset.    ",
    "    Timer starts    ",
    "   when finished.   "
]

READY_LINES = [
    "   Game Begins in   ",
    "    5 Seconds...    ",
    "",
    "   Are You Ready?   "
]



I2C_ADDR = 39   # 20x4 Screen
#I2C_ADDR = 63  # 16x2 Screen
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

LCD_LOCK = _thread.allocate_lock()
FINAL_TIME = 0

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)
lcd = pico_i2c_lcd.I2cLcd(i2c,I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

buzzer = machine.PWM(machine.Pin(5))
buzzer.duty_u16(0)

WINNING_SCORE = 0
TIMER = 300
TIMER_HARD = 180
TIMER_EASY = 420
GAME_TIME = TIMER
GAME_MODE = ""
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

RED_BUTTON = 10
GREEN_BUTTON = 9
YELLOW_BUTTON = 8
BLUE_BUTTON = 7
WHITE_BUTTON = 6

RED_TOGGLE = 16
GREEN_TOGGLE = 17
ORANGE_TOGGLE = 18
BLUE_TOGGLE = 19
WHITE_TOGGLE = 20

RED_ROCKER = 15
GREEN_ROCKER = 14
BLUE_ROCKER = 13
ORANGE_ROCKER = 12

YELLOW_WIRE = 21
BLACK_WIRE = 22
GREEN_WIRE = 26
BLUE_WIRE = 27

BUTTONS = [RED_BUTTON, GREEN_BUTTON, YELLOW_BUTTON, BLUE_BUTTON, WHITE_BUTTON]
TOGGLES = [RED_TOGGLE, GREEN_TOGGLE, ORANGE_TOGGLE, BLUE_TOGGLE, WHITE_TOGGLE]
ROCKERS = [RED_ROCKER, GREEN_ROCKER, BLUE_ROCKER, ORANGE_ROCKER]
WIRES = [YELLOW_WIRE, GREEN_WIRE, BLUE_WIRE, BLACK_WIRE]

combined = [BUTTONS, TOGGLES, ROCKERS]
SWITCHES = [item for sublist in combined for item in sublist]