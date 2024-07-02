import utime, pico_i2c_lcd
from variables import *

I2C_ADDR = 63
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)
lcd = pico_i2c_lcd.I2cLcd(i2c,I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


def startup():
    global TIMER
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Cipher Solver")
    lcd.move_to(0, 1)
    lcd.putstr(f"Escape Games  v{VERSION}")
    utime.sleep(3)
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Starting Game...")
    lcd.move_to(0, 1)
    lcd.putstr("Are You Ready?")
    utime.sleep(7)

    lcd.clear()
    lcd.move_to(0, 1)
    lcd.putstr(f"S/N:{game['serial']}")
    TIMER += utime.time()


def read_pin(pin):
    s = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    return s.value()


def set_timer_thread():
    time_remaining = TIMER
    while still_playing():
        time_remaining = TIMER - utime.time()

        current_minutes = time_remaining // 60
        current_seconds = time_remaining % 60
        if current_seconds < 10:
            current_seconds = f"0{current_seconds}"
        lcd.move_to(0, 0)
        lcd.putstr(f"Countdown:  {current_minutes}:{current_seconds}")


def game_win():
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("CONGRATULATIONS!")
    lcd.move_to(1,1)
    lcd.putstr("BOMB DEFUSED!")
    RED_LED.value(0)
    BLUE_LED.value(0)
    GREEN_LED.value(1)
    return False


def game_lose():
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("BOOOOOOOOOOOOOM!")
    lcd.move_to(3, 1)
    lcd.putstr("YOU LOSE!")
    RED_LED.value(1)
    BLUE_LED.value(0)
    GREEN_LED.value(0)
    return False


def flash_colors(sequence):
    RED_LED.value(0)
    BLUE_LED.value(0)
    GREEN_LED.value(0)

    for color in sequence:
        color.value(1)
        utime.sleep(.2)
        color.value(0)
        utime.sleep(.2)


def check_pins():
    total = 0
    for switch in SWITCHES:
        s = read_pin(switch)
        if s == 0:
            if switch in game["winners_on"]:
                total += 1
            else:
                total += 20
    for wire in WIRES:
        w = read_pin(wire)
        if w == 0:
            if wire in game["winners_on"]:
                total += 1
            else:
                total += 20
    return total


def still_playing():
    score = check_pins()
    if score > WINNING_SCORE + ERROR_MOD:
        return False
    elif utime.time() > TIMER:
        return False
    else:
        return True
