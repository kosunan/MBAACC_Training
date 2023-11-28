import os
import time
from ctypes import windll
from utils.common import (
    cmd_cursor_move,
    ex_cmd_enable,
    changeFontSize,
    high_precision_sleep,
)

from Fn_01_Address_Table_and_utill import game_system_instance
from Fn_01_Address_Table_and_utill import character_state_instances
from Fn_01_Address_Table_and_utill import save_State_Manager_instance
from Fn_03_action_handler import ActionHandler
from Fn_04_Cui_cnt import template_view, training_display, FrameIndicator


action_Handler_instance = ActionHandler(
    game_system_instance, save_State_Manager_instance
)

ex_cmd_enable()
changeFontSize(7, 14)
os.system("mode con: cols=160 lines=11")
os.system("cls")
os.system("title MBAACC_Training 1.3")
print("\x1b[1;1H" + "\x1b[?25l")
windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする

print(template_view())


def getActiveCharacterState(char_states, idx):
    if char_states[idx].switch_flag.read_memory() == 0:
        char_states[idx].fetchGameData()
        return char_states[idx]
    else:
        # スイッチされたキャラクターの状態を取得
        char_states[idx + 2].fetchGameData()
        return char_states[idx + 2]


frameIndicator = FrameIndicator(80)


global_frame_count = 0
previous_frame_count = -1
FRAME_DELAY = 0.003  # フレーム遅延の定数
FRAME_DURATION = 0.016  # 目標とするループの総実行時間（秒）
while True:
    start_time = time.perf_counter()  # ループ開始時刻
    gamemode = game_system_instance.game_mode_check()
    if gamemode != 20:
        action_Handler_instance.action_handle()
    elif gamemode == 20:
        action_Handler_instance.is_save_flag = False

    # タイマーチェック
    global_frame_count = game_system_instance.timer_check()
    if global_frame_count == 1:
        frameIndicator.reset_bars()

    if global_frame_count != previous_frame_count:
        # フレームが切り替わったときの処理をここに記述
        previous_frame_count = global_frame_count  # 前のフレーム数を更新

        # フレームが切り替わった直後はゲームの状態が不安定なため、少し待つ

        high_precision_sleep(FRAME_DELAY)
        # ゲームシステムのデータ取得
        game_system_instance.fetchGameData()  # ゲームデータの取得

        # キャラの各種ステータス取得
        act_state_p1 = getActiveCharacterState(character_state_instances, 0)
        act_state_p2 = getActiveCharacterState(character_state_instances, 1)

        p1_bar_obj, p2_bar_obj = frameIndicator.state_bar_cre(
            act_state_p1, act_state_p2
        )

        p1_adv = frameIndicator.p1_bar_obj.advantage
        p2_adv = frameIndicator.p2_bar_obj.advantage

        if p1_adv != 0:
            adv_value = p1_adv

        elif p2_adv != 0:
            adv_value = p2_adv * -1
        else:
            # どちらも値が0の場合の処理
            adv_value = 0

        para_state = training_display(
            game_system_instance, act_state_p1, act_state_p2, adv_value
        )
        para_state += cmd_cursor_move(4, 1) + p1_bar_obj[0]
        para_state += cmd_cursor_move(5, 1) + p1_bar_obj[1]
        para_state += cmd_cursor_move(6, 1) + p1_bar_obj[2]

        para_state += cmd_cursor_move(8, 1) + p2_bar_obj[0]
        para_state += cmd_cursor_move(9, 1) + p2_bar_obj[1]
        para_state += cmd_cursor_move(10, 1) + p2_bar_obj[2]
        print(para_state)

        end_time = time.perf_counter()  # ループ終了時刻
        elapsed_time = end_time - start_time  # 処理にかかった時間

        sleep_time = FRAME_DURATION - elapsed_time  # 待機する時間
        if sleep_time > 0:
            high_precision_sleep(sleep_time)
            # print(cmd_cursor_move(10, 1) + str(sleep_time))
