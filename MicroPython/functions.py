import utime
import machine
import variables as v
from font import *

def startup():
    v.lcd.clear()
    v.lcd.move_to(0, 0)
    v.lcd.putstr("Cipher Solver")
    v.lcd.move_to(0, 1)
    v.lcd.putstr(f"Escape Games  v{v.VERSION}")
    utime.sleep(3)

    v.lcd.clear()
    v.lcd.move_to(0, 0)
    v.lcd.putstr("Starting Game...")
    v.lcd.move_to(0, 1)
    v.lcd.putstr("Are You Ready?")
    utime.sleep(7)

    v.lcd.clear()
    v.lcd.move_to(0, 3)
    v.lcd.putstr(f"S/N:{v.game['serial']}")

    v.TIMER += utime.time()

def read_pin(pin):
    s = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    return s.value()

def set_timer_thread():
    custom_character()

    v.lcd.move_to(0, 0)
    v.lcd.putstr("Count")
    v.lcd.move_to(0, 1)
    v.lcd.putstr("down:")

    last_shown_sec = None

    while v.playing and still_playing():
        time_remaining = max(0, v.TIMER - utime.time())

        current_minutes = str(time_remaining // 60)
        current_seconds = time_remaining % 60

        if current_seconds != last_shown_sec:
            last_shown_sec = current_seconds
            if current_seconds < 10:
                sec_str = f"0{current_seconds}"
            else:
                sec_str = str(current_seconds)

            print_character(0, current_minutes)
            print_character(1, ":")
            print_character(2, sec_str[0])
            print_character(3, sec_str[1])

        utime.sleep_ms(100)

def game_win():
    v.playing = False
    utime.sleep_ms(150)
    v.lcd.clear()
    v.lcd.move_to(0, 0)
    v.lcd.putstr("CONGRATULATIONS!")
    v.lcd.move_to(1, 1)
    v.lcd.putstr("BOMB DEFUSED!")
    v.RED_LED.value(0)
    v.BLUE_LED.value(0)
    v.GREEN_LED.value(1)
    return False
    

def game_lose():
    v.playing = False
    utime.sleep_ms(150)
    v.lcd.clear()
    v.lcd.move_to(0, 0)
    v.lcd.putstr("BOOOOOOOOOOOOOM!")
    v.lcd.move_to(3, 1)
    v.lcd.putstr("YOU LOSE!")
    v.RED_LED.value(1)
    v.BLUE_LED.value(0)
    v.GREEN_LED.value(0)
    return False

def flash_colors(sequence):
    v.RED_LED.value(0)
    v.BLUE_LED.value(0)
    v.GREEN_LED.value(0)

    for color in sequence:
        if not v.playing or not still_playing():
            break
        color.value(1)
        utime.sleep_ms(150)
        color.value(0)
        utime.sleep_ms(150)

def check_pins():
    total = 0
    for switch in v.SWITCHES:
        s = read_pin(switch)
        if s == 0:
            if switch in v.game["winners_on"]:
                total += 1
            else:
                total += v.ERROR_MOD

    for wire in v.WIRES:
        w = read_pin(wire)
        if w == 1:
            if wire in v.game["winners_on"]:
                total += 1
            else:
                total += v.ERROR_MOD

    return total

def still_playing():
    if not v.playing:
        return False

    score = check_pins()
    if score > v.WINNING_SCORE + v.ERROR_MOD:
        return False
    elif utime.time() > v.TIMER:
        return False
    else:
        return True

def custom_character():
    v.lcd.custom_char(0, bytearray(font0))
    v.lcd.custom_char(1, bytearray(font1))
    v.lcd.custom_char(2, bytearray(font2))
    v.lcd.custom_char(3, bytearray(font3))
    v.lcd.custom_char(4, bytearray(font4))
    v.lcd.custom_char(5, bytearray(font5))
    v.lcd.custom_char(6, bytearray(font6))
    v.lcd.custom_char(7, bytearray(font7))

def print_character(slot, number):
    character = custom_font_dict[number]
    v.lcd.move_to(font_position[slot], 0)
    v.lcd.putchar(character[0])
    v.lcd.move_to(font_position[slot] + 1, 0)
    v.lcd.putchar(character[1])
    v.lcd.move_to(font_position[slot], 1)
    v.lcd.putchar(character[2])
    v.lcd.move_to(font_position[slot] + 1, 1)
    v.lcd.putchar(character[3])