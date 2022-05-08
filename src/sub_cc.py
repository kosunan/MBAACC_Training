from ctypes import windll, wintypes, byref
from struct import unpack, pack
import os
import time
import copy
import ctypes
import keyboard
import psutil

import cfg_cc
import ad_cc
import save_cc
cfg = cfg_cc
ad = ad_cc
save = save_cc

wintypes = ctypes.wintypes
windll = ctypes.windll
create_string_buffer = ctypes.create_string_buffer
byref = ctypes.byref
WriteMem = windll.kernel32.WriteProcessMemory
ReadMem = windll.kernel32.ReadProcessMemory
OpenProcess = windll.kernel32.OpenProcess
Module32Next = windll.kernel32.Module32Next
Module32First = windll.kernel32.Module32First
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CloseHandle = windll.kernel32.CloseHandle
sizeof = ctypes.sizeof


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize",             wintypes.DWORD),
        ("th32ModuleID",       wintypes.DWORD),
        ("th32ProcessID",      wintypes.DWORD),
        ("GlblcntUsage",       wintypes.DWORD),
        ("ProccntUsage",       wintypes.DWORD),
        ("modBaseAddr",        ctypes.POINTER(wintypes.BYTE)),
        ("modBaseSize",        wintypes.DWORD),
        ("hModule",            wintypes.HMODULE),
        ("szModule",           ctypes.c_byte * 256),
        ("szExePath",          ctypes.c_byte * 260),
    ]


def pidget():
    dict_pids = {
        p.info["name"]: p.info["pid"]
        for p in psutil.process_iter(attrs=["name", "pid"])
    }
    return dict_pids


def get_base_addres(dict_pids):
    cfg.pid = 0
    while cfg.pid == 0:
        try:
            cfg.pid = dict_pids["MBAA.exe"]
        except:
            os.system('cls')
            print("Waiting for MBAA to start")

    cfg.h_pro = OpenProcess(0x1F0FFF, False, cfg.pid)

    # MODULEENTRY32を取得
    snapshot = CreateToolhelp32Snapshot(0x00000008, cfg.pid)

    lpme = MODULEENTRY32()
    lpme.dwSize = sizeof(lpme)

    res = Module32First(snapshot, byref(lpme))

    while cfg.pid != lpme.th32ProcessID:
        res = Module32Next(snapshot, byref(lpme))

    b_baseAddr = create_string_buffer(8)
    b_baseAddr.raw = lpme.modBaseAddr

    cfg.base_ad = unpack('q', b_baseAddr.raw)[0]


def r_mem(ad, b_obj):
    ReadMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)


def w_mem(ad, b_obj):
    WriteMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)


def ex_cmd_enable():
    INVALID_HANDLE_VALUE = -1
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    ENABLE_LVB_GRID_WORLDWIDE = 0x0010

    hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    if hOut == INVALID_HANDLE_VALUE:
        return False
    dwMode = wintypes.DWORD()
    if windll.kernel32.GetConsoleMode(hOut, byref(dwMode)) == 0:
        return False
    dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    # dwMode.value |= ENABLE_LVB_GRID_WORLDWIDE
    if windll.kernel32.SetConsoleMode(hOut, dwMode) == 0:
        return False
    return True

def situationReset():

    # 状況をリセット
    w_mem(ad.RESET_AD, b'\xFF')

def pause():

    # 一時停止
    w_mem(ad.ANTEN_STOP_AD, b'\xff')

def play():

    # 再生
    w_mem(ad.ANTEN_STOP_AD, b'\x00')


def situationCheck():
    # 状況チェック
    r_mem(ad.FN1_KEY_AD, cfg.b_fn1_key)
    r_mem(ad.FN2_KEY_AD, cfg.b_fn2_key)

    r_mem(ad.DUMMY_STATUS_AD, cfg.b_dummy_status_ad)
    r_mem(ad.RECORDING_MODE_AD, cfg.b_recording_mode_ad)
    r_mem(ad.ANTEN_STOP_AD, cfg.b_stop)

    for n in cfg.P_info:
        r_mem(n.anten_stop_ad, n.b_anten_stop)
        r_mem(n.atk_ad, n.b_atk)
        r_mem(n.gauge_ad, n.b_gauge)
        r_mem(n.hitstop_ad, n.b_hitstop)
        r_mem(n.motion_ad, n.b_motion)
        r_mem(n.motion_type_ad, n.b_motion_type)
        r_mem(n.x_ad, n.b_x)
        r_mem(n.stop_ad, n.b_stop)
        r_mem(n.step_inv_ad, n.b_step_inv)
    r_mem(ad.DAMAGE_AD, cfg.b_damage)


def situationMem():

    # 状況を記憶
    save.P_info = copy.deepcopy(cfg.P_info)

    for n in cfg.P_info:
        r_mem(n.dmp_ad, n.b_dmp)



    r_mem( ad.OBJ_AD, save.b_obj)
    r_mem( ad.STOP_SITUATION_AD, save.b_stop_situation)

    r_mem( ad.ANTEN_STOP_AD, save.b_stop)
    r_mem( ad.DAMAGE_AD, save.b_damage)
    r_mem( ad.DAMAGE2_AD, save.b_damage2)

    r_mem( ad.CAM1_X_AD, save.b_cam1_x)
    r_mem( ad.CAM1_Y_AD, save.b_cam2_x)
    r_mem( ad.CAM2_X_AD, save.b_cam1_y)
    r_mem( ad.CAM2_Y_AD, save.b_cam2_y)

def situationWrit():
    # 状況を再現
    save.P_info = copy.deepcopy(cfg.P_info)

    for n in cfg.P_info:
        w_mem(n.dmp_ad, n.b_dmp)

    w_mem( ad.OBJ_AD, save.b_obj)
    w_mem( ad.STOP_SITUATION_AD, save.b_stop_situation)

    w_mem( ad.ANTEN_STOP_AD, save.b_stop)
    w_mem( ad.DAMAGE_AD, save.b_damage)
    w_mem( ad.DAMAGE2_AD, save.b_damage2)

    w_mem( ad.CAM1_X_AD, save.b_cam1_x)
    w_mem( ad.CAM1_Y_AD, save.b_cam2_x)
    w_mem( ad.CAM2_X_AD, save.b_cam1_y)
    w_mem( ad.CAM2_Y_AD, save.b_cam2_y)


def MAX_Damage_ini():
    w_mem(ad.MAX_DAMAGE_AD, b'\x00\x00\x00\x00')


def view_st():

    # 全体フレームの取得
    overall_calc()

    # 技の発生フレームの取得
    firstActive_calc()

    # 硬直差の取得
    advantage_calc()

    # キャラの状況推移表示
    if (
        cfg.p1.motion_type != 0 or
        cfg.p2.motion_type != 0 or
        cfg.p1.hitstop != 0 or
        cfg.p2.hitstop != 0 or
        cfg.p1.hit != 0 or
        cfg.p2.hit != 0
    ):
        cfg.reset_flag = 0
        cfg.Bar_flag = 1
        cfg.interval = 0
    else:
        cfg.Bar_flag = 0
        cfg.interval += 1

    # バーリセット判定
    determineReset()

    # 表示管理　表示するものが無くても前回の表示からインターバルの間は無条件で表示する
    if cfg.interval_time >= cfg.interval and cfg.reset_flag == 0:
        if cfg.Bar80_flag == 0:
            cfg.Bar_flag = 1

    # 暗転判定処理
    if cfg.stop != 0:
        cfg.anten += 1
    elif cfg.p1.anten_stop != 0 or cfg.p2.anten_stop != 0:
        cfg.anten += 1
    else:
        cfg.anten = 0

    # ヒットストップ処理
    if (cfg.p1.hitstop != 0 and cfg.p2.hitstop != 0):
        cfg.hitstop += 1
    elif (cfg.p1.hitstop == 0 or cfg.p2.hitstop == 0):
        cfg.hitstop = 0



    # バー追加処理
    if cfg.Bar_flag == 1:
        bar_add()


def advantage_calc():
    if cfg.p1.hit == 0 and cfg.p2.hit == 0 and cfg.p1.motion_type == 0 and cfg.p2.motion_type == 0:
        cfg.DataFlag1 = 0

    if (cfg.p1.hit != 0 or cfg.p1.motion_type != 0) and (cfg.p2.hit != 0 or cfg.p2.motion_type != 0):
        cfg.DataFlag1 = 1
        cfg.yuuriF = 0

    if cfg.DataFlag1 == 1:

        # 有利フレーム検証
        if (cfg.p1.hit == 0 and cfg.p1.motion_type == 0) and (cfg.p2.hit != 0 or cfg.p2.motion_type != 0):
            cfg.yuuriF += 1

        # 不利フレーム検証
        if (cfg.p1.hit != 0 or cfg.p1.motion_type != 0) and (cfg.p2.hit == 0 and cfg.p2.motion_type == 0):
            cfg.yuuriF -= 1


def overall_calc():
    # 全体フレームの取得
    if cfg.p1.motion != 0:
        cfg.p1.zen = cfg.p1.motion

    if cfg.p2.motion != 0:
        cfg.p2.zen = cfg.p2.motion


def bar_add():

    DEF = '\x1b[0m'

    FC_DEF = '\x1b[39m'
    BC_DEF = '\x1b[49m'

    atk = "\x1b[38;5;255m" + "\x1b[48;5;160m"
    mot = "\x1b[38;5;255m" + "\x1b[48;5;010m"
    grd = '\x1b[0m' + "\x1b[48;5;250m"
    nog = "\x1b[38;5;250m" + "\x1b[48;5;000m"
    fre = "\x1b[38;5;234m" + "\x1b[48;5;000m"
    non = "\x1b[38;5;148m" + "\x1b[48;5;201m"

    if cfg.anten == 0 and cfg.hitstop <= 1:
        cfg.Bar_num += 1
        if cfg.Bar_num == cfg.bar_range:
            cfg.Bar_num = 0
            cfg.Bar80_flag = 1

    for n in cfg.p_info:
        num = ""

        if n.b_atk.raw != b'\x00':  # 攻撃判定を出しているとき
            font = atk
        elif n.step_inv != 0:  # バックステップ無敵中
            font = "\x1b[48;5;015m"

        elif n.motion != 0:  # モーション途中
            font = mot

        elif n.hit != 0:  # ガードorヒット硬直中
            font = grd

        elif n.motion_type != 0:  # ガードできないとき
            font = nog

        elif n.motion == 0:  # 何もしていないとき
            font = fre

        else:  # いずれにも当てはまらないとき
            font = non

        # ジャンプ移行中
        if n.motion_type == 34 or n.motion_type == 35 or n.motion_type == 36 or n.motion_type == 37:
            if n.motion != 0:
                font = "\x1b[38;5;000m" + "\x1b[48;5;011m"
            elif n.motion == 0:
                n.motion_type = 0
                font = fre
        # 起き上がり中
        if n.motion_type == 32 or n.motion_type == 33:
            font = "\x1b[38;5;255m" + "\x1b[48;5;055m"

        if n.motion != 0:
            num = str(n.motion)
        else:
            font = fre
            num = str(n.motion_type)

        if n.hit != 0:
            num = str(n.hit)

        if num == '0' and cfg.DataFlag1 == 1:
            if n == cfg.p_info[0] or n == cfg.p_info[1]:
                font = "\x1b[38;5;244m" + "\x1b[48;5;000m"
                num = str(abs(cfg.yuuriF))

        n.barlist_1[cfg.Bar_num] = font + num.rjust(2, " ")[-2:] + DEF


def bar_ini():
    cfg.reset_flag = 1
    cfg.p1.Bar_1 = ""
    cfg.p2.Bar_1 = ""
    cfg.p3.Bar_1 = ""
    cfg.p4.Bar_1 = ""
    cfg.st_Bar = ""
    cfg.Bar_num = 0
    cfg.interval = 0
    cfg.interval2 = 0
    cfg.bar_ini_flag2 = 0
    cfg.Bar80_flag = 0
    cfg.interval_time = 80

    for n in range(cfg.bar_range):
        cfg.p1.barlist_1[n] = ""
        cfg.p2.barlist_1[n] = ""
        cfg.p3.barlist_1[n] = ""
        cfg.p4.barlist_1[n] = ""
        cfg.st_barlist[n] = ""


def firstActive_calc():
    # 計測開始の確認
    if cfg.p2.hitstop != 0 and cfg.p1.act_flag == 0 and cfg.p1.hit == 0:
        cfg.p1.act = cfg.p1.zen
        cfg.p1.act_flag = 1

    if cfg.p1.hitstop != 0 and cfg.p2.act_flag == 0 and cfg.p2.hit == 0:
        cfg.p2.act = cfg.p2.zen
        cfg.p2.act_flag = 1

    if cfg.p1.motion == 0 and cfg.p1.atk == 0:
        cfg.p1.act_flag = 0

    if cfg.p2.motion == 0 and cfg.p2.atk == 0:
        cfg.p2.act_flag = 0


def b_unpack(d_obj):
    num = 0
    num = len(d_obj)
    if num == 1:
        return unpack('b', d_obj.raw)[0]
    elif num == 2:
        return unpack('h', d_obj.raw)[0]
    elif num == 4:
        return unpack('l', d_obj.raw)[0]
    else:
        return 1000


def get_values():
    negligible_number = [0, 10, 11, 12,
                         13, 14, 15, 18,
                         20, 16, 594, 17]
    hit_number = [904, 900, 901,
                  906, 29, 26,
                  903, 907, 30,
                  350]

    cfg.fn1_key = b_unpack(cfg.b_fn1_key)
    cfg.fn2_key = b_unpack(cfg.b_fn2_key)
    cfg.game_mode = b_unpack(cfg.b_game_mode)
    cfg.dummy_status = b_unpack(cfg.b_dummy_status_ad)
    cfg.recording_mode = b_unpack(cfg.b_recording_mode_ad)
    cfg.stop = b_unpack(cfg.b_stop)

    for n in cfg.P_info:
        n.x = b_unpack(n.b_x)
        if n.motion_type != 0:
            n.motion_type_old = n.motion_type
        n.motion_type = b_unpack(n.b_motion_type)

        n.motion = b_unpack(n.b_motion)
        n.atk = b_unpack(n.b_atk)
        n.inv = b_unpack(n.b_inv)
        n.step_inv = b_unpack(n.b_step_inv)

        n.hitstop_old = n.hitstop
        n.hitstop = b_unpack(n.b_hitstop)
        n.hit = b_unpack(n.b_hit)
        n.noguard = b_unpack(n.b_noguard)
        n.anten_stop = b_unpack(n.b_anten_stop)
        n.anten_stop2_old = n.anten_stop2
        n.anten_stop2 = b_unpack(n.b_anten_stop2)

        n.gauge = b_unpack(n.b_gauge)
        n.moon = b_unpack(n.b_moon)
        n.ukemi1 = b_unpack(n.b_ukemi1)
        n.ukemi2 = b_unpack(n.b_ukemi2)
        for m in negligible_number:
            if n.motion_type == m:
                n.motion = 0
                n.motion_type = 0
                break

        for m in hit_number:
            if n.motion_type == m:
                n.hit = 1
                n.motion_type = 0
                n.motion = 0
                break

    cfg.p_info = cfg.P_info
    cfg.p1 = cfg.P_info[0]
    cfg.p2 = cfg.P_info[1]
    cfg.p3 = cfg.P_info[2]
    cfg.p4 = cfg.P_info[3]


def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    x_p1 = str(cfg.p1.x).rjust(8, " ")
    x_p2 = str(cfg.p2.x).rjust(8, " ")

    zen_P1 = str(cfg.p1.zen).rjust(3, " ")
    zen_P2 = str(cfg.p2.zen).rjust(3, " ")

    gauge_p1 = str('{:.02f}'.format(cfg.p1.gauge / 100)).rjust(7, " ")
    gauge_p2 = str('{:.02f}'.format(cfg.p2.gauge / 100)).rjust(7, " ")

    act_P1 = str(cfg.p1.act).rjust(3, " ")
    act_P2 = str(cfg.p2.act).rjust(3, " ")

    # yuuriF = str(cfg.yuuriF).rjust(4, " ")
    yuuriF = str(cfg.yuuriF).rjust(7, " ")

    kyori = cfg.p1.x - cfg.p2.x

    cfg.p1.Bar_1 = ""
    cfg.p2.Bar_1 = ""
    cfg.p3.Bar_1 = ""
    cfg.p4.Bar_1 = ""

    cfg.st_Bar = ""

    temp = cfg.Bar_num

    for n in range(cfg.bar_range):
        temp += 1
        if temp == cfg.bar_range:
            temp = 0
        cfg.p1.Bar_1 += cfg.p1.barlist_1[temp]
        cfg.p2.Bar_1 += cfg.p2.barlist_1[temp]
        cfg.p3.Bar_1 += cfg.p3.barlist_1[temp]
        cfg.p4.Bar_1 += cfg.p4.barlist_1[temp]

        cfg.st_Bar += cfg.st_barlist[temp]

    if kyori < 0:
        kyori = kyori * -1
    kyori = kyori / (18724 * 2)
    kyori = str(kyori)[:5]

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    state_str += '1P|Position' + x_p1
    state_str += ' FirstActive' + act_P1
    state_str += ' Overall' + zen_P1
    state_str += ' Circuit' + gauge_p1 + '%'

    state_str += '   [F1]Reset [F2]Save [F3]Moon switch [F4]Max damage ini' + END

    state_str += '2P|Position' + x_p2
    state_str += ' FirstActive' + act_P2
    state_str += ' Overall' + zen_P2
    state_str += ' Circuit' + gauge_p2 + '%'
    state_str += END

    state_str += '  |Advantage' + yuuriF
    state_str += ' Proration' + "%"
    state_str += ' Untec'
    state_str += '  Range ' + kyori + 'M' + END

    state_str += '  | 1 2 3 4 5 6 7 8 91011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980' + END
    state_str += '1P|' + cfg.p1.Bar_1 + END
    state_str += '2P|' + cfg.p2.Bar_1 + END

    print(state_str)
    degug_view()


def degug_view():
    if cfg.debug_flag == 1:
        # os.system('mode con: cols=166 lines=15')
        debug_str_p1 = "f_timer " + str(cfg.f_timer).rjust(7, " ")
        debug_str_p2 = "Bar_num " + str(cfg.Bar_num).rjust(7, " ")

        debug_str_p1 += "motion_type " + str(cfg.p1.motion_type).rjust(7, " ")
        debug_str_p2 += "motion_type " + str(cfg.p2.motion_type).rjust(7, " ")
        debug_str_p1 += " motion " + str(cfg.p1.motion).rjust(7, " ")
        debug_str_p2 += " motion " + str(cfg.p2.motion).rjust(7, " ")
        debug_str_p1 += " anten_stop " + str(cfg.p1.anten_stop).rjust(7, " ")
        debug_str_p2 += " anten_stop " + str(cfg.p2.anten_stop).rjust(7, " ")
        debug_str_p1 += " hitstop " + str(cfg.p1.hitstop).rjust(7, " ")
        debug_str_p2 += " hitstop " + str(cfg.p2.hitstop).rjust(7, " ")
        debug_str_p1 += " anten " + str(cfg.anten).rjust(7, " ")
        debug_str_p1 += " stop " + str(cfg.stop).rjust(7, " ")
        debug_str_p1 += " dummy_status " + str(cfg.dummy_status).rjust(7, " ")
        debug_str_p1 += " fn2_key " + str(cfg.fn2_key).rjust(7, " ")

        print(debug_str_p1)
        print(debug_str_p2)


def determineReset():
    bar_ini_flag = 0

    if cfg.Bar80_flag == 1:
        cfg.interval_time = 1

    # インターバル後の初期化
    if cfg.interval_time <= cfg.interval:
        cfg.bar_ini_flag2 = 1

    # 表示するときリセット
    if cfg.bar_ini_flag2 == 1 and cfg.Bar_flag == 1:
        bar_ini_flag = 1

    cfg.interval2 += 1

    cfg.old_mftp = cfg.p1.motion_type

    # 即時リセット
    if bar_ini_flag == 1:
        bar_ini()

def mode_check():
    r_mem(ad.GAME_MODE_AD, cfg.b_game_mode)
    cfg.game_mode = b_unpack(cfg.b_game_mode)
    
def timer_check():
    r_mem(ad.TIMER_AD, cfg.b_timer)
    cfg.f_timer = b_unpack(cfg.b_timer)
