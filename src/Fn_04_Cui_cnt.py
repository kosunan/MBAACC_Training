import os
from utils.common import cmd_cursor_move, get_font, changeFontSize, ex_cmd_enable

import keyboard
import Cf_01_color_code
from Cf_02_state_num import (
    hit_state_num,
    ignore_state_num,
    jump_state_num,
)

ex_cmd_enable()

color_code_dict = Cf_01_color_code.color_dict
template_view_flag = 0


def template_view():
    state_str = ""
    global template_view_flag
    if template_view_flag == 0:
        template_view_flag = 1
        underline = "\x1b[4m"
        end = "\x1b[0m"

        #               10        20        30        40        50        60        70        80        90       100
        #      123456789112345678921234567893123456789412345678951234567896123456789712345678981234567899123456789012345678991
        st1 = "adv|x_rng|y_rng|"

        state_str += cmd_cursor_move(1, 1) + st1

        st3 = ""
        for i in range(1, 81):
            n_1 = str(i).rjust(2, " ")[0:1]
            n_2 = str(i).rjust(2, " ")[1:2]

            if n_2 != "0":
                n_1 = " "

                font = color_code_dict["tape_color1"]
            elif n_2 == "0":
                font = color_code_dict["tape_color2"]
            st3 += underline + font + n_1 + n_2 + "\x1b[0m"

        state_str += cmd_cursor_move(3, 1) + st3 + end

        state_str += cmd_cursor_move(1, 120)
        state_str += "motion " + color_code_dict["motion_color"] + "01" + end
        state_str += "  atk " + color_code_dict["attack_color"] + "01" + end
        state_str += "  stun " + color_code_dict["hit_stun_color"] + "01" + end
        state_str += "  jmp " + color_code_dict["jump_color"] + "01" + end
        state_str += " air " + underline + "01" + end

        state_str += cmd_cursor_move(2, 120)
        state_str += " seeld " + color_code_dict["shield_color"] + "01" + end
        state_str += "  inv " + color_code_dict["invincible_color"] + "01" + end
        state_str += "  stop " + color_code_dict["hitstop_color"] + "01" + end
        state_str += " armor" + color_code_dict["bunker_color"] + "01" + end

    return state_str


def get_and_format_character_data(character):
    x = character.x_position.int_data
    y = character.y_position_1.int_data
    sx = character.x_speed.int_data
    sy = character.y_speed.int_data
    hp = character.health.int_data
    pct = character.circuit_value.int_data
    mot = character.motion_pattern.int_data
    mot_num = character.remaining_motion_frames.int_data

    keyDir = character.numeric_keypad_directions.int_data

    return f"x{x:6}|y{y:6}|sx{sx:5}|sy{sy:5}|hp{hp:5}|mot{mot:3}|mot_num{mot_num:4}|keyDir{keyDir:4}|"


def training_display(game_system_instance, act_st_1, act_st_2, adv_frame):
    state_str = ""
    underline = "\x1b[4m"
    end = "\x1b[0m"

    # キャラクターのデータ取得
    st1 = get_and_format_character_data(act_st_1)
    st2 = get_and_format_character_data(act_st_2)

    # act = 00
    adv = adv_frame
    unt = 000
    x_rng = act_st_1.x_position.int_data - act_st_2.x_position.int_data
    y_rng = act_st_1.y_position_1.int_data - act_st_2.y_position_1.int_data

    st3 = f"{adv:3}|{abs(x_rng):5}|{abs(y_rng):5}|"

    state_str += cmd_cursor_move(1, 17) + st1 + end
    state_str += cmd_cursor_move(2, 17) + st2 + end
    state_str += cmd_cursor_move(2, 1) + st3 + end

    if keyboard.is_pressed("F1"):
        f1 = "\x1b[007m" + "[F1]SaveState " + "\x1b[0m"
    else:
        f1 = "[F1]SaveState "

    if keyboard.is_pressed("F2"):
        f2 = "\x1b[007m" + "[F2]loadState" + "\x1b[0m"
    else:
        f2 = "[F2]loadState"
    state_str += cmd_cursor_move(1, 87) + f1 + f2

    return state_str


class Element_Bar:
    def __init__(self, indicator_length):
        self.indicator_length = indicator_length
        self.bar1 = [""] * indicator_length
        self.bar2 = [""] * indicator_length
        self.bar3 = [""] * indicator_length
        self.advantage = 0
        self.element_active_count1 = 0
        self.element_active_count2 = 0
        self.last_color1 = ""
        self.last_color2 = ""

    def adv_calc(self):
        self.advantage = self.element_active_count1

    def update_bars(
        self, color1, color2, floating, bar_index, is_full_count_flag, key_dir
    ):
        end = "\x1b[0m"

        # カラーコードが非アクティブ状態の場合はカウンターを0に、それ以外はカウンターを増やす
        if color1 == "\x1b[0m":
            self.element_active_count1 = 0
        elif color1 == self.last_color1:
            self.element_active_count1 += 1
        else:
            self.element_active_count1 = 1
            self.last_color1 = color1

        if color2 == "\x1b[0m":
            self.element_active_count2 = 0
        elif color2 == self.last_color2:
            self.element_active_count2 += 1
        else:
            self.element_active_count2 = 1
            self.last_color2 = color2

        if color1 == color_code_dict["adv_color"]:
            self.adv_calc()

        # カウンターの値をフォーマットして、先頭の '0' を空白に置き換える
        def format_counter(value):
            if value == 0:
                return "  "
            formatted = f"{value % 100:02}"
            return formatted if formatted[0] != "0" else " " + formatted[1]

        count_str1 = format_counter(self.element_active_count1)
        count_str2 = format_counter(self.element_active_count2)
        key_dir_st = format_counter(key_dir)

        key_dir_color = color_code_dict["keyDir_color"] if key_dir != 0 else ""

        self.bar1[bar_index] = "".join([color1, floating, count_str1, end])
        self.bar2[bar_index] = "".join([color2, count_str2, end])
        self.bar3[bar_index] = "".join([key_dir_color, key_dir_st, end])

        # バーの表示順を調整
        if is_full_count_flag:
            display_bar1 = self.bar1[bar_index + 1 :] + self.bar1[: bar_index + 1]
            display_bar2 = self.bar2[bar_index + 1 :] + self.bar2[: bar_index + 1]
            display_bar3 = self.bar3[bar_index + 1 :] + self.bar3[: bar_index + 1]
        else:
            display_bar1 = self.bar1
            display_bar2 = self.bar2
            display_bar3 = self.bar3

        return (
            "".join(display_bar1),
            "".join(display_bar2),
            "".join(display_bar3),
        )

    def reset_bars(self):
        self.bar1 = ["  "] * self.indicator_length
        self.bar2 = ["  "] * self.indicator_length
        self.bar3 = ["  "] * self.indicator_length
        self.element_active_count1 = 0
        self.element_active_count2 = 0
        self.last_color1 = ""
        self.last_color2 = ""


class FrameIndicator:
    def __init__(self, indicator_length):
        self.indicator_length = indicator_length
        self.bar_index = 0
        self.is_indicator_full_count_flag = False
        self.is_indicator_active_flag = False
        self.initial_count = 30
        self.indicator_not_active_count = 31
        self.initial_flag = False  # イニシャル処理が必要かどうかのフラグ

        self.advantage = 0
        self.p1_bar_obj = Element_Bar(indicator_length)
        self.p2_bar_obj = Element_Bar(indicator_length)
        self.p1_old_motion_frames = -1
        self.p2_old_motion_frames = -1
        self.is_adv_flag = False

    def reset_bars(self):
        # リストとインデックスを初期化する
        self.p1_bar_obj.reset_bars()
        self.p2_bar_obj.reset_bars()
        self.bar_index = 0
        self.is_indicator_full_count_flag = False

    def check_both_characters_stopped(self, character1, character2):
        """両キャラクターが同時に停止しているかをチェックし、
        停止していない場合はフレームを更新するメソッド"""

        motion_frame_p1 = character1.remaining_motion_frames.int_data
        motion_frame_p2 = character2.remaining_motion_frames.int_data

        # 個々のキャラクターがヒットストップ中かどうかをチェック
        hitstop_p1 = character1.hitstop_value.int_data > 0
        hitstop_p2 = character2.hitstop_value.int_data > 0

        # 個々のキャラクターが停止しているかどうかのフラグを設定
        stopped_p1 = hitstop_p1
        stopped_p2 = hitstop_p2

        if motion_frame_p1 != self.p1_old_motion_frames:
            stopped_p1 = False
        if motion_frame_p2 != self.p2_old_motion_frames:
            stopped_p2 = False

        if motion_frame_p1 == 0 and motion_frame_p2 == 0:
            stopped_p1 = False
            stopped_p2 = False

        # 両方のキャラクターが同時に停止しているかどうかを判定
        both_stopped = stopped_p1 and stopped_p2

        # 停止していない場合はフレームを更新
        if not both_stopped:
            self.p1_old_motion_frames = motion_frame_p1
            self.p2_old_motion_frames = motion_frame_p2

        return both_stopped

    def check_active_state(
        self, color1_p1, color2_p1, color1_p2, color2_p2, keyDir_p1, keyDir_p2
    ):
        if (
            color1_p1 == "\x1b[0m"
            and color2_p1 == "\x1b[0m"
            and color1_p2 == "\x1b[0m"
            and color2_p2 == "\x1b[0m"
            and keyDir_p1 == 0
            and keyDir_p2 == 0
        ):
            self.indicator_not_active_count += 1
            self.is_indicator_active_flag = False
        else:
            self.is_indicator_active_flag = True
            if self.initial_flag:
                self.reset_bars()
                self.initial_flag = False
            self.indicator_not_active_count = 0

    def get_advantage_value(self):
        if self.p1_bar_obj.advantage != 0:
            self.advantage = self.p1_bar_obj.advantage
            return
        elif self.p2_bar_obj.advantage != 0:
            self.advantage = self.p2_bar_obj.advantage * -1
            return

        self.advantage = 0

    def process_exclusive_state(self, color1_p1, color1_p2):
        if (color1_p1 != "\x1b[0m") != (color1_p2 != "\x1b[0m") and self.is_adv_flag:
            if color1_p1 != "\x1b[0m":
                color1_p2 = color_code_dict["adv_color"]
                self.p1_bar_obj.advantage = 0
            else:
                color1_p1 = color_code_dict["adv_color"]
                self.p2_bar_obj.advantage = 0

        elif (color1_p1 != "\x1b[0m") and (color1_p2 != "\x1b[0m"):
            self.is_adv_flag = True
        elif (color1_p1 == "\x1b[0m") and (color1_p2 == "\x1b[0m"):
            self.is_adv_flag = False
        return color1_p1, color1_p2

    def update_bars_state(self, color1, color2, floating, bar_obj, key_dir):
        display_bar1, display_bar2, display_bar3 = bar_obj.update_bars(
            color1,
            color2,
            floating,
            self.bar_index,
            self.is_indicator_full_count_flag,
            key_dir,
        )
        return display_bar1, display_bar2, display_bar3

    def update_bar_index(self, both_characters_stopped):
        if (
            self.is_indicator_active_flag
            or self.indicator_not_active_count <= self.initial_count
        ) and not both_characters_stopped:
            if self.bar_index == self.indicator_length - 1:
                self.is_indicator_full_count_flag = True
                self.bar_index = 0
            else:
                self.bar_index += 1

    def state_bar_cre(self, character1, character2):
        color1_p1, color2_p1, floating_p1 = get_color_code(character1)
        color1_p2, color2_p2, floating_p2 = get_color_code(character2)
        keyDir_p1 = character1.numeric_keypad_directions.int_data
        keyDir_p2 = character2.numeric_keypad_directions.int_data

        self.check_active_state(
            color1_p1, color2_p1, color1_p2, color2_p2, keyDir_p1, keyDir_p2
        )
        color1_p1, color1_p2 = self.process_exclusive_state(color1_p1, color1_p2)

        # 更新されたバーの状態を取得
        display_p1_bar1, display_p1_bar2, display_p1_bar3 = self.update_bars_state(
            color1_p1, color2_p1, floating_p1, self.p1_bar_obj, keyDir_p1
        )
        display_p2_bar1, display_p2_bar2, display_p2_bar3 = self.update_bars_state(
            color1_p2, color2_p2, floating_p2, self.p2_bar_obj, keyDir_p2
        )

        both_characters_stopped = self.check_both_characters_stopped(
            character1, character2
        )

        # イニシャルフラグの設定
        if self.indicator_not_active_count > self.initial_count:
            self.initial_flag = True
            # 両キャラクターが停止している場合、バーインデックスの更新を行わない

        # バーインデックスの更新
        self.update_bar_index(both_characters_stopped)
        self.get_advantage_value()
        display_p1 = (display_p1_bar1, display_p1_bar2, display_p1_bar3)
        display_p2 = (display_p2_bar1, display_p2_bar2, display_p2_bar3)
        return (display_p1, display_p2)


def get_color_code(character):
    underline = "\x1b[4m"
    floating = ""

    # color1 の決定
    if character.remaining_motion_frames.int_data != 0:
        if character.attack_data.int_data == 10:
            color1 = color_code_dict["shield_color"]
        elif character.attack_data.int_data == 12:
            color1 = color_code_dict["bunker_color"]
        elif character.motion_pattern.int_data in hit_state_num:
            color1 = color_code_dict["hit_stun_color"]
        elif character.motion_pattern.int_data in jump_state_num:
            color1 = color_code_dict["jump_color"]
        elif (
            character.attack_data.int_data in [0, 1]
            or character.step_invincibility.int_data != 0
        ):
            color1 = color_code_dict["invincible_color"]
        elif character.motion_pattern.int_data not in ignore_state_num:
            color1 = color_code_dict["motion_color"]
        else:
            color1 = "\x1b[0m"
    elif character.motion_pattern.int_data == 350:
        color1 = color_code_dict["hit_stun_color"]
    else:
        color1 = "\x1b[0m"

    # color2 の決定
    color2 = (
        color_code_dict["hitstop_color"]
        if character.hitstop_value.int_data > 0
        else color_code_dict["attack_color"]
        if character.attack_status.int_data != 0
        else "\x1b[0m"
    )

    # floating の決定
    if any(
        [
            character.float_flag.int_data != 0,
            character.y_position_1.int_data != 0,
            character.y_position_2.int_data != 0,
        ]
    ):
        floating = underline

    return (color1, color2, floating)
