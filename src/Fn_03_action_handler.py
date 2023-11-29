import keyboard


class ActionHandler:
    def __init__(self, game_system_obj, save_State_obj):
        self.game_system_fnc_obj = game_system_obj
        self.save_State_fnc_obj = save_State_obj
        self.f1_pressed_last_frame = False
        self.f2_pressed_last_frame = False
        self.is_pressed_key = False
        self.is_save_flag = False

    def action_handle(self):
        if self.game_system_fnc_obj.game_mode_check() == 20:
            self.is_save_flag = False
            return
        fnc1_but = self.game_system_fnc_obj.fn1_key.read_memory()
        fnc2_but = self.game_system_fnc_obj.fn2_key.read_memory()
        dmy_st = self.game_system_fnc_obj.dummy_st.int_data

        is_f1_pressed = keyboard.is_pressed("F1") or fnc1_but >= 1

        if keyboard.is_pressed("F2") or (
            fnc2_but >= 1 and (dmy_st == 5 or dmy_st == -1)
        ):
            self.game_system_fnc_obj.game_reset()
            self.is_pressed_key = True

        # F1キーが押された瞬間を検出
        if is_f1_pressed and not self.f1_pressed_last_frame:
            self.action_f1()
            self.is_save_flag = True
            self.is_pressed_key = True
        self.f1_pressed_last_frame = is_f1_pressed

        # ゲームがリセットされてタイマーが1の時
        if self.game_system_fnc_obj.timer_check() == 1 and self.is_save_flag == True:
            self.action_f2()

        # キーが離された場合
        if not is_f1_pressed and self.is_pressed_key:
            self.is_pressed_key = False
            self.game_system_fnc_obj.play()

    def action_f1(self):
        self.save_State_fnc_obj.saveGameState()
        self.game_system_fnc_obj.pause()

    def action_f2(self):
        self.save_State_fnc_obj.loadGameState()
        self.game_system_fnc_obj.comb_after_timer_reset()
