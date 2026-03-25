import utime
import machine
import variables as v
from font import *

DEBUG = False
SOUND_ON = True
TEST_MODE = False

BUTTON_LETTERS = {
    v.RED_BUTTON: "R",
    v.GREEN_BUTTON: "G",
    v.YELLOW_BUTTON: "Y",
    v.BLUE_BUTTON: "B",
    v.WHITE_BUTTON: "W",
}

TOGGLE_LETTERS = {
    v.RED_TOGGLE: "R",
    v.GREEN_TOGGLE: "G",
    v.ORANGE_TOGGLE: "O",
    v.BLUE_TOGGLE: "B",
    v.WHITE_TOGGLE: "W",
}

ROCKER_LETTERS = {
    v.RED_ROCKER: "R",
    v.GREEN_ROCKER: "G",
    v.BLUE_ROCKER: "B",
    v.ORANGE_ROCKER: "O",
}

WIRE_LETTERS = {
    v.YELLOW_WIRE: "Y",
    v.GREEN_WIRE: "G",
    v.BLUE_WIRE: "B",
    v.BLACK_WIRE: "K",
}


def buzzer_off():
    v.buzzer.duty_u16(0)

def play_tone(freq, ms, duty=20000):
    v.buzzer.freq(freq)
    v.buzzer.duty_u16(duty)
    utime.sleep_ms(ms)
    v.buzzer.duty_u16(0)

def countdown_tick(time_remaining):
    # Normal tick above 30, faster / sharper below 30
    if SOUND_ON:
        play_tone(2400, 35)

def explosion_sound():
    # Descending harsh burst
    for freq in (2000, 1700, 1400, 1100, 900, 700, 500, 300):
        play_tone(freq, 60, 30000)
    utime.sleep_ms(80)
    for _ in range(3):
        play_tone(120, 120, 35000)
        utime.sleep_ms(30)

def victory_jingle():
    for freq, dur in (
        (1047, 120),  # C
        (1319, 120),  # E
        (1568, 120),  # G
        (2093, 220),  # C
    ):
        play_tone(freq, dur, 22000)
        utime.sleep_ms(30)

def get_changed_status_text():
    b_correct = sum(1 for x in v.BUTTONS if x in v.game["winners_on"] and read_pin(x) == 0)
    t_correct = sum(1 for x in v.TOGGLES if x in v.game["winners_on"] and read_pin(x) == 0)
    r_correct = sum(1 for x in v.ROCKERS if x in v.game["winners_on"] and read_pin(x) == 0)
    w_correct = sum(1 for x in v.WIRES if x in v.game["winners_on"] and read_pin(x) == 1)

    b_changed = sum(1 for x in v.BUTTONS if read_pin(x) == 0)
    t_changed = sum(1 for x in v.TOGGLES if read_pin(x) == 0)
    r_changed = sum(1 for x in v.ROCKERS if read_pin(x) == 0)
    w_changed = sum(1 for x in v.WIRES if read_pin(x) == 1)

    total_changed = b_changed + t_changed + r_changed + w_changed
    if DEBUG:
        return f"B{b_correct}/5T{t_correct}/5R{r_correct}/4W{w_correct}/4 {total_changed}"
    else:
        return ""


def check_debug():
    global DEBUG
    counter = 0
    if read_pin(v.GREEN_BUTTON) == 0:
        counter += 1
    if read_pin(v.BLUE_BUTTON) == 0:
        counter += 1
    if read_pin(v.RED_BUTTON) == 0:
        counter += 1
    if read_pin(v.YELLOW_BUTTON) == 0:
        counter += 1
    if read_pin(v.WHITE_BUTTON) == 0:
        counter += 1
    if counter == 5:
        DEBUG = True
        test_mode()

def check_quiet_mode():
    global SOUND_ON
    if read_pin(v.WHITE_TOGGLE) == 0:
        SOUND_ON = False

def detect_difficulty_mode():
    hard_on = read_pin(v.RED_TOGGLE) == 0
    easy_on = read_pin(v.GREEN_TOGGLE) == 0

    if hard_on and not easy_on:
        v.GAME_MODE = "Expert"
        v.GAME_TIME = v.TIMER_HARD
    elif easy_on and not hard_on:
        v.GAME_MODE = "Novice"
        v.GAME_TIME = v.TIMER_EASY
    else:
        v.GAME_MODE = "Normal"
        v.GAME_TIME = v.TIMER

def led_letter(led):
    if led == v.RED_LED:
        return "R"
    elif led == v.GREEN_LED:
        return "G"
    elif led == v.BLUE_LED:
        return "B"
    return "?"

def get_led_sequence_text():
    return "".join(led_letter(x) for x in v.game["led_seq"])

def get_remaining_time_text():
    remaining = max(0, int(v.FINAL_TIME))
    minutes = remaining // 60
    seconds = remaining % 60
    return f"{minutes}:{seconds:02d}"

def get_solution_summary():
    buttons = ""
    toggles = ""
    rockers = ""
    wires = ""

    for item in v.game["winners_on"]:
        if item in BUTTON_LETTERS:
            buttons += BUTTON_LETTERS[item]
        elif item in TOGGLE_LETTERS:
            toggles += TOGGLE_LETTERS[item]
        elif item in ROCKER_LETTERS:
            rockers += ROCKER_LETTERS[item]
        elif item in WIRE_LETTERS:
            wires += WIRE_LETTERS[item]

    return f"B{buttons}-T{toggles}-R{rockers}-W{wires}"

def lcd_write_lines(lines):
    v.LCD_LOCK.acquire()
    try:
        v.lcd.clear()
        for row, text in enumerate(lines[:4]):
            v.lcd.move_to(0, row)
            v.lcd.putstr(str(text)[:20])
    finally:
        v.LCD_LOCK.release()


def test_mode():
    lcd_write_lines([
    "Debug Mode.",
    "Swap all switches.",
    "You have 30 seconds.",
    "",
    ])
    utime.sleep(30)
    button_errors = "B:"
    toggle_errors = "T:"
    rocker_errors = "R:"
    wire_errors = "W:"
    for item in BUTTON_LETTERS.keys():
        if read_pin(item) != 0:
            button_errors += BUTTON_LETTERS[item]    
    for item in TOGGLE_LETTERS.keys():
        if read_pin(item) != 0:
            toggle_errors += TOGGLE_LETTERS[item]
    for item in ROCKER_LETTERS.keys():
        if read_pin(item) != 0:
            rocker_errors += ROCKER_LETTERS[item]
    for item in WIRE_LETTERS.keys():
        if read_pin(item) != 1:
            wire_errors += WIRE_LETTERS[item]
    lcd_write_lines([
        button_errors,
        toggle_errors,
        rocker_errors,
        wire_errors
        ])
    utime.sleep(10)
    
    
def startup():
    lcd_write_lines(v.INTRO_LINES)
    utime.sleep(3)
    soundmsg = "    Sound FX: On    "
    if not SOUND_ON:
        soundmsg = "    Sound FX Off    "
    lcd_write_lines([
        f"    {v.GAME_MODE} Mode.    ",
        f"{soundmsg}",
        "",
        " Reset All Switches ",
        ])
    utime.sleep(3)

    if check_pins() > 0:
        lcd_write_lines(v.WAITING_LINES)
    
    while check_pins() > 0:
        utime.sleep_ms(200)

    for remaining in range(v.READY_DELAY, 0, -1):
        lcd_write_lines([
            "   Game Begins in   ",
            f"    {remaining} Seconds...    ",
            "",
            "   Are You Ready?   "
        ])
        utime.sleep(1)
    
    lcd_write_lines([
        "",
        "",
        "",
        f"S/N:{v.game['serial']}"
    ])

def read_pin(pin):
    s = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    return s.value()

def set_timer_thread():
    custom_character()

    v.LCD_LOCK.acquire()
    try:
        v.lcd.move_to(0, 0)
        v.lcd.putstr("Count")
        v.lcd.move_to(0, 1)
        v.lcd.putstr("down:")
        v.lcd.move_to(0, 2)
        v.lcd.putstr(" " * 20)
        v.lcd.move_to(0, 2)
        v.lcd.putstr(get_changed_status_text()[:20])
    finally:
        v.LCD_LOCK.release()

    last_shown_sec = None
    last_half_sec = None

    while v.playing and still_playing():
        time_remaining = max(0, v.TIMER - utime.time())
        v.FINAL_TIME = time_remaining

        current_minutes = str(time_remaining // 60)
        current_seconds = time_remaining % 60
        half_sec_marker = int(time_remaining * 2)

        # Main once-per-second tick
        if current_seconds != last_shown_sec:
            last_shown_sec = current_seconds

            if time_remaining > 0:
                countdown_tick(time_remaining)

            if current_seconds < 10:
                sec_str = f"0{current_seconds}"
            else:
                sec_str = str(current_seconds)

            if not v.playing:
                buzzer_off()
                return

            v.LCD_LOCK.acquire()
            try:
                if not v.playing:
                    buzzer_off()
                    return
                print_character(0, current_minutes)
                print_character(1, ":")
                print_character(2, sec_str[0])
                print_character(3, sec_str[1])

                v.lcd.move_to(0, 2)
                v.lcd.putstr(" " * 20)
                v.lcd.move_to(0, 2)
                v.lcd.putstr(get_changed_status_text()[:20])
            finally:
                v.LCD_LOCK.release()

        # Extra half-second tick under 30 seconds
        # if time_remaining < 30 and half_sec_marker != last_half_sec:
            # last_half_sec = half_sec_marker
            # if half_sec_marker % 2 == 1 and time_remaining > 0:
                # play_tone(2400, 20)

        utime.sleep_ms(50)

    buzzer_off()

def game_win():
    v.FINAL_TIME = max(0, v.TIMER - utime.time())
    v.playing = False
    utime.sleep_ms(150)

    lcd_write_lines([
        "CONGRATULATIONS!",
        "BOMB DEFUSED!",
        f"TIME LEFT {get_remaining_time_text()}",
        f"S/N:{v.game['serial']}"
    ])

    v.RED_LED.value(0)
    v.BLUE_LED.value(0)
    v.GREEN_LED.value(1)
    return False
    

def game_lose():
    v.FINAL_TIME = max(0, v.TIMER - utime.time())
    v.playing = False
    utime.sleep_ms(150)

    led_text = get_led_sequence_text()
    summary = get_solution_summary()

    lcd_write_lines([
        "       BOOM!!",
        "     YOU LOSE!!",
        f"S/N:{v.game['serial']} {led_text}",
        summary
    ])

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