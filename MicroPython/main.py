import utime
import _thread
import variables as v
import game_builder
import functions

functions.detect_difficulty_mode()
functions.check_debug()
functions.check_quiet_mode()
game_builder.game_selector()
functions.startup()

setup_timer = utime.time()
wait_time = 0

def main_loop():
    v.playing = True
    v.WINNING_SCORE = len(v.game["winners_on"])

    v.TIMER = v.GAME_TIME + utime.time()
    v.FINAL_TIME = v.GAME_TIME

    _thread.start_new_thread(functions.set_timer_thread, ())

    print(v.game["winners_on"])

    while v.playing:
        utime.sleep(1)
        total = functions.check_pins()

        if total == v.WINNING_SCORE:
            if functions.SOUND_ON:
                functions.victory_jingle()
            v.playing = functions.game_win()

        elif not functions.still_playing():
            if functions.SOUND_ON:
                functions.explosion_sound()
            v.playing = functions.game_lose()
            

        else:
            functions.flash_colors(v.game["led_seq"])

main_loop()