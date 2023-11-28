import utils.process_memory_access
from utils.process_memory_access import MemoryBlock
import ctypes


# MemoryBlock初期化処理 ベースアドレスの設定
# 指定されたプロセスが起動するまで待機する
utils.process_memory_access.wait_process("MBAA.exe")


class Game_System_Address_Table:
    def __init__(self):
        # フレームデータのメモリアドレスとサイズのペアを定義
        frame_data_pairs = [
            # 各タプルは('データ名', メモリアドレス, サイズ)の形式
            ("timer", 0x162A40, 4),
            ("fn1_key", 0x37144C, 1),
            ("fn2_key", 0x37144D, 1),
            ("dummy_st", 0x34D7F8, 2),
            ("recording_mode", 0x155137, 2),
            ("stop_flag", 0x162A48, 1),
            ("game_mode", 0x14EEE8, 2),
            ("training_menu_pause", 0x162A64, 2),
            ("max_damage", 0x157E0C, 4),
            ("circuit_position", 0x15DEF0, 2),
            ("round_reset", 0x15DEC3, 1),
            ("comb_after_timer", 0x36E708, 2),
            ("disable_fn1_1_AD", 0x41F654, 12),
            ("disable_fn1_2_AD", 0x41F652, 2),
        ]

        # 初期化: メモリアクセス用のフレームデータペアリストを空のリストで初期化
        self.memory_access_frame_data_pairs_list = []

        # frame_data_pairsの各要素に対して繰り返し処理
        for name, addr, size in frame_data_pairs:
            # MemoryBlockインスタンスを生成
            # addr: メモリアドレス, size: データサイズ,
            # memory_access_frame_data_pairs_list: メモリブロックのリスト
            mem_block = MemoryBlock(addr, size)
            self.memory_access_frame_data_pairs_list.append(mem_block)

            # 生成したMemoryBlockを現在のインスタンスに属性として追加
            # 属性名はframe_data_pairsのname要素に基づく
            setattr(self, name, mem_block)

        # 特定の機能(fn1_keyとfn2_key)を無効化
        self.disable_fn1_1_AD.write_absolute(0x41F654, b"\x90" * 12)
        self.disable_fn1_2_AD.write_absolute(0x41F654, b"\x90" * 2)

    def fetchGameData(self):
        # ゲームデータをメモリから読み込む
        # for memory_block_instance in self.memory_access_frame_data_pairs_list:
        #     memory_block_instance.read_memory()
        self.timer.read_memory()
        self.fn1_key.read_memory()
        self.fn2_key.read_memory()
        self.dummy_st.read_memory()
        self.game_mode.read_memory()

    def game_reset(self):
        self.round_reset.write_memory(b"\xff")

    def pause(self):
        # ゲームを一時停止

        self.stop_flag.write_memory(b"\xff")

    def play(self):
        # ゲームを再開
        self.stop_flag.write_memory(b"\x00")

    def game_mode_check(self):
        # 現在のゲームモードを確認
        return self.game_mode.read_memory()

    def timer_check(self):
        # ゲームのタイマーを確認
        return self.timer.read_memory()

    def initialize_max_damage(self):
        # 最大ダメージの値を初期化
        self.max_damage.write_memory(b"\x00\x00\x00\x00")

    def comb_after_timer_reset(self):
        # コンボ後のタイマーをリセット
        self.comb_after_timer.write_memory(b"\xff")


class Character_State_Address_Table:
    # キャラクター構造体のサイズを定義
    PLR_STRUCT_SIZE = 0xAFC  # 3084
    # 1Pデータの開始位置を定義
    DAT_P1_AD = 0x155140

    def __init__(self, player_num):
        base_ad_size = self.PLR_STRUCT_SIZE * (player_num - 1)

        # 各キャラクター状態のメモリアドレスとサイズのペアを定義
        frame_data_pairs = [
            # 各タプルは('状態名', メモリアドレス, サイズ)の形式
            ("motion_pattern", 0x155140, 2),
            ("character_timer", 0x155220, 4),
            ("attack_status", 0x155454, 4),
            ("step_invincibility", 0x1552B5, 1),
            ("x_position", 0x155238, 4),
            ("y_position_1", 0x15523C, 4),
            ("y_position_2", 0x155248, 4),
            ("x_speed", 0x15524C, 4),
            ("y_speed", 0x155250, 4),
            ("numeric_keypad_directions", 0x15541A, 1),
            ("health", 0x1551EC, 2),
            ("red_health", 0x1551F0, 2),
            ("float_flag", 0x155256, 2),
            ("circuit_value", 0x155210, 4),
            ("hitstop_value", 0x1552A2, 1),
            ("attack_data_pointer", 0x155450, 4),
            ("attack_data", 0x00000, 1),
        ]

        switch_flag_ad = 0x1552A8 if player_num % 2 == 1 else 0x1552A8 + 0xA5C
        blackout_pause_ad = 0x158908 + ((player_num - 1) % 2) * self.PLR_STRUCT_SIZE

        frame_data_pairs.append(("switch_flag", switch_flag_ad, 1))
        frame_data_pairs.append(("blackout_pause", blackout_pause_ad, 1))

        if player_num == 1 or player_num == 3:
            remaining_motion_frames_ad = 0x157FC0
        elif player_num == 2 or player_num == 4:
            remaining_motion_frames_ad = 0x1581CC

        frame_data_pairs.append(
            ("remaining_motion_frames", remaining_motion_frames_ad, 4)
        )

        # 初期化: メモリアクセス用のフレームデータペアリストを空のリストで初期化
        self.memory_access_frame_data_pairs_list = []

        # MemoryBlockインスタンスを生成
        # addr: メモリアドレス, size: データサイズ,
        # memory_access_frame_data_pairs_list: メモリブロックのリスト
        for name, addr, size in frame_data_pairs:
            if name in [
                "switch_flag",
                "blackout_pause",
                "remaining_motion_frames",
            ]:
                mem_block = MemoryBlock(addr, size)
            else:
                mem_block = MemoryBlock(base_ad_size + addr, size)

            self.memory_access_frame_data_pairs_list.append(mem_block)

            # 生成したMemoryBlockを現在のインスタンスに属性として追加
            # 属性名はframe_data_pairsのname要素に基づく
            setattr(self, name, mem_block)

    def fetchGameData(self):
        for memory_block_instance in self.memory_access_frame_data_pairs_list:
            memory_block_instance.read_memory()
        self.set_attack_data()

    def set_attack_data(self):
        self.attack_data.read_absolute(self.attack_data_pointer.int_data + 0x42)


class Save_State_Manager:
    # キャラクター構造体のサイズを定義
    PLR_STRUCT_SIZE = 0xAFC  # 3084
    # 1Pデータの開始位置を定義
    DAT_P1_AD = 0x155140

    def __init__(self):
        # メモリアドレスとサイズのペアを定義
        save_state_pairs = [
            ("cam1_x", 0x164B14, 4),
            ("cam2_x", 0x15DEC4, 4),
            ("cam1_y", 0x164B18, 4),
            ("cam2_y", 0x15DEC8, 4),
            ("objects", 0x27BD70, 74576),
            ("stoppage_status", 0x158600, 1632),
            ("damage", 0x157DD8, 52),
            ("damage_2", 0x157E10, 1004),
            ("shift_control_flag_1", 0x157DB8, 4),
            ("shift_control_flag_2", 0x157DBC, 4),
            ("dmp_data", self.DAT_P1_AD, 971),
            ("dmp_data", self.DAT_P1_AD + (self.PLR_STRUCT_SIZE * 1), 971),
            ("dmp_data", self.DAT_P1_AD + (self.PLR_STRUCT_SIZE * 2), 971),
            ("dmp_data", self.DAT_P1_AD + (self.PLR_STRUCT_SIZE * 3), 971),
        ]

        # 初期化: メモリアクセスペアリストを空のリストで初期化
        self.memory_access_save_state_pairs_list = []

        # save_state_pairsの各要素に対して繰り返し処理
        for name, addr, size in save_state_pairs:
            # MemoryBlockインスタンスを生成
            # addr: メモリアドレス, size: データサイズ,
            # memory_access_save_state_pairs_list: メモリブロックのリスト
            mem_block = MemoryBlock(addr, size)
            self.memory_access_save_state_pairs_list.append(mem_block)

            # 生成したMemoryBlockを現在のインスタンスに属性として追加
            # 属性名はsave_state_pairsのname要素に基づく
            setattr(self, name, mem_block)

    def saveGameState(self):
        # ゲームの現在の状態をメモリから読み込み保存
        for memory_block_instance in self.memory_access_save_state_pairs_list:
            memory_block_instance.read_memory()

    def loadGameState(self):
        # 保存されたデータをゲームのメモリに書き込む
        for memory_block_instance in self.memory_access_save_state_pairs_list:
            memory_block_instance.write_memory()


game_system_instance = Game_System_Address_Table()
character_state_instances = [
    Character_State_Address_Table(1),
    Character_State_Address_Table(2),
    Character_State_Address_Table(3),
    Character_State_Address_Table(4),
]
save_State_Manager_instance = Save_State_Manager()
