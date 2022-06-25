from ctypes import windll
from struct import unpack
import os
import time
import keyboard
import cfg_cc
import ad_cc

import sub_cc
ad = ad_cc
cfg = cfg_cc
sub = sub_cc

sub.ex_cmd_enable()
os.system('mode con: cols=166 lines=10')
os.system('cls')
os.system('title MBAACC_Training 1.2.6')
print('\x1b[1;1H' + '\x1b[?25l')
windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする

# 変数初期化
save_flag = 0
flag1 = 0
start_time = time.time()


def function_key():

    global flag1
    global save_flag

    # セーブデータリセット
    if keyboard.is_pressed("F1"):
        if flag1 == 0:
            save_flag = 0
        elif flag1 == 100:
            sub.MAX_Damage_ini()
        flag1 += 1
    # 状況記憶
    elif keyboard.is_pressed("F2") or cfg.fn1_key.num == 1 or cfg.fn1_key.num == 3:
        if flag1 == 0:
            sub.situationMem()
            sub.pause()

            save_flag = 1
            flag1 = 1

    elif cfg.fn2_key.num == 1 or cfg.fn2_key.num == 3:
        if flag1 == 0:
            flag1 = 1
            if cfg.dummy_st.num == 5 or cfg.dummy_st.num == -1:
                sub.situationReset()
            sub.w_mem(ad.COMB_AFTER_TIMER_AD, b'\xFF')

    # デバッグ表示
    elif (keyboard.is_pressed("9")) and (keyboard.is_pressed("0")):
        if cfg.debug_flag == 0:
            cfg.debug_flag = 1
            os.system('mode con: cols=166 lines=15')

        elif cfg.debug_flag == 1:
            cfg.debug_flag = 0
            os.system('mode con: cols=166 lines=10')

        time.sleep(0.3)

    elif flag1 >= 1:
        flag1 = 0
        sub.play()


###############################################################
# メイン関数
###############################################################
# 実行中のすべてのＩＤ＋プロセス名取得

# ベースアドレス取得
sub.get_base_addres()

# FN1ボタンの無効化
sub.disable_fn1()

while 1:
    time.sleep(0.003)

    # MODEチェック
    sub.mode_check()

    if cfg.game_mode.num == 20:
        save_flag = 0

    function_key()

    # タイマーチェック
    sub.timer_check()

    # フレームの切り替わりを監視
    if (cfg.f_timer != cfg.f_timer2):

        cfg.f_timer2 = cfg.f_timer
        time.sleep(0.001)

        # 各種数値の取得
        sub.situationCheck()

        # ゲーム状況の取得
        sub.view_st()

        if cfg.f_timer == 1:
            sub.bar_ini()

            if save_flag == 1:
                # 状況再現
                sub.situationWrit()
    sub.view()
