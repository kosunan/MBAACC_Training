import os
import time
from ctypes import windll
from utils.common import (
    cmd_cursor_move,
    ex_cmd_enable,
    changeFontSize,
    high_precision_sleep,
    high_precision_sleep_until,
)
from Fn_01_Address_Table_and_utill import (
    game_system_instance,
    character_state_instances,
    save_State_Manager_instance,
)
from Fn_03_action_handler import ActionHandler
from Fn_04_Cui_cnt import template_view, training_display, FrameIndicator


def setup_environment():
    ex_cmd_enable()
    changeFontSize(7, 14)
    os.system("mode con: cols=160 lines=11")
    os.system("cls")
    os.system("title MBAACC_Training 1.3")
    print("\x1b[1;1H" + "\x1b[?25l")
    windll.winmm.timeBeginPeriod(1)


def get_active_character_state(char_states, idx):
    offset = 2 if char_states[idx].switch_flag.read_memory() else 0
    char_states[idx + offset].fetchGameData()
    return char_states[idx + offset]


def display_game_state(game_system, char1_state, char2_state, frame_indicator):
    p1_bar_obj, p2_bar_obj = frame_indicator.state_bar_cre(char1_state, char2_state)
    para_state = training_display(
        game_system, char1_state, char2_state, frame_indicator.advantage
    )
    for i in range(3):
        para_state += (
            cmd_cursor_move(4 + i, 1)
            + p1_bar_obj[i]
            + cmd_cursor_move(8 + i, 1)
            + p2_bar_obj[i]
        )
    para_state += template_view()
    print(para_state)


def main_loop():
    frame_indicator = FrameIndicator(80)
    action_handler = ActionHandler(game_system_instance, save_State_Manager_instance)
    previous_frame_count = 0
    global_frame_count = 0
    FRAME_DURATION = 0.016
    while True:
        while global_frame_count == previous_frame_count:
            global_frame_count = game_system_instance.timer_check()
            pass

        start_time = time.perf_counter()
        end_time = start_time + FRAME_DURATION
        previous_frame_count = global_frame_count

        if global_frame_count <= 1:
            frame_indicator.reset_bars()

        high_precision_sleep(0.003)
        game_system_instance.fetchGameData()

        char1_state = get_active_character_state(character_state_instances, 0)
        char2_state = get_active_character_state(character_state_instances, 1)
        display_game_state(
            game_system_instance, char1_state, char2_state, frame_indicator
        )
        action_handler.action_handle()

        high_precision_sleep_until(end_time)


setup_environment()
main_loop()
