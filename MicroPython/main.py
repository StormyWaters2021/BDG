from variables import *
import game_builder, utime, _thread, functions

game_builder.game_selector()    # Choose a random configuration from a list
functions.startup()

setup_timer = utime.time()
wait_time = 0


def main_loop():
    global playing
    WINNING_SCORE = len(game["winners_on"])
    _thread.start_new_thread(functions.set_timer_thread, ())
    print(game["winners_on"])
    while playing:
        utime.sleep(1)
        total = functions.check_pins()

        if total == WINNING_SCORE:
            playing = functions.game_win()

        if not functions.still_playing():
            functions.game_lose()

        else:
            functions.flash_colors(game["led_seq"])


main_loop()
