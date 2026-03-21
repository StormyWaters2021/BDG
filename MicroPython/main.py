import utime
import _thread
import variables as v
import game_builder
import functions

game_builder.game_selector()
functions.startup()

setup_timer = utime.time()
wait_time = 0

def main_loop():
    v.playing = True
    v.WINNING_SCORE = len(v.game["winners_on"])

    _thread.start_new_thread(functions.set_timer_thread, ())

    print(v.game["winners_on"])

    while v.playing:
        utime.sleep(1)
        total = functions.check_pins()

        if total == v.WINNING_SCORE:
            v.playing = functions.game_win()

        elif not functions.still_playing():
            v.playing = functions.game_lose()

        else:
            functions.flash_colors(v.game["led_seq"])

main_loop()