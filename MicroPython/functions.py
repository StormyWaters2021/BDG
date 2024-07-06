import utime
from variables import *
from font import *

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
    lcd.move_to(0, 3)
    lcd.putstr(f"S/N:{game['serial']}")
    TIMER += utime.time()


def read_pin(pin):
    s = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    return s.value()


def set_timer_thread():
    time_remaining = TIMER
    custom_character()
    lcd.move_to(0, 0)
    lcd.putstr("Count")
    lcd.move_to(0, 1)
    lcd.putstr("down:")
    while still_playing():
        time_remaining = TIMER - utime.time()

        current_minutes = str(time_remaining // 60)
        current_seconds = time_remaining % 60
        if current_seconds < 10:
            current_seconds = f"0{current_seconds}"
        else:
            current_seconds = str(current_seconds)
        print_character(0, current_minutes)
        print_character(1, ":")
        print_character(2, current_seconds[0])
        print_character(3, current_seconds[1])


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


def custom_character():
    lcd.custom_char(0, bytearray(font0))
    lcd.custom_char(1, bytearray(font1))
    lcd.custom_char(2, bytearray(font2))
    lcd.custom_char(3, bytearray(font3))
    lcd.custom_char(4, bytearray(font4))
    lcd.custom_char(5, bytearray(font5))
    lcd.custom_char(6, bytearray(font6))
    lcd.custom_char(7, bytearray(font7))


def print_character(slot, number):
    character = custom_font_dict[number]
    lcd.move_to(font_position[slot], 0)
    lcd.putchar(character[0])
    lcd.move_to(font_position[slot]+1, 0)
    lcd.putchar(character[1])
    lcd.move_to(font_position[slot], 1)
    lcd.putchar(character[2])
    lcd.move_to(font_position[slot]+1, 1)
    lcd.putchar(character[3])
