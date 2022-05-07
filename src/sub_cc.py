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


def pause():

    # 一時停止
    r_mem(ad.TRAINING_PAUSE_AD, b'\xff')


def play():

    # 再生
    r_mem(ad.TRAINING_PAUSE_AD, b'\x00')


def situationCheck():
    # 状況チェック
    r_mem(ad.TIMER_AD, cfg.b_timer)
    r_mem(ad.FN1_KEY_AD, cfg.b_fn1_key)
    r_mem(ad.FN2_KEY_AD, cfg.b_fn2_key)
    r_mem(ad.GAME_MODE_AD, cfg.b_game_mode)
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
        r_mem(n.stop_ad, cfg.b_stop)

    r_mem(ad.DAMAGE_AD, cfg.b_damage)


def situationMem():

    # 状況を記憶
    r_mem(ad.CAM_AD, save.b_cam)
    save.P_info = copy.deepcopy(cfg.P_info)


def situationWrit():
    # 状況を再現
    # 状況を再現
    w_mem(ad.CAM_AD, save.b_cam)

    for n in save.P_info:
        w_mem(n.gauge_ad, n.b_gauge)
        w_mem(n.x_ad, n.b_x)

    r_mem(ad.DAT_P1_AD, save.dat_p1)
    r_mem(ad.DAT_P2_AD, save.dat_p2)
    r_mem(ad.DAT_P3_AD, save.dat_p3)
    r_mem(ad.DAT_P4_AD, save.dat_p4)

    r_mem(ad.CAM1_X_AD, save.cam1_x)
    r_mem(ad.CAM1_Y_AD, save.cam2_x)
    r_mem(ad.CAM2_X_AD, save.cam1_y)
    r_mem(ad.CAM2_Y_AD, save.cam2_y)


def situationWrit2():
    # 状況を再現
    r_mem(ad.SAVE_BASE_AD, save.save_data, save.data_size2)
    r_mem(ad.DAT_P1_AD, save.P1_data1, save.data_size)
    r_mem(ad.DAT_P2_AD, save.P2_data1, save.data_size)


def moon_change():

    if cfg.b_m_st_p1.raw == b'\x00':
        r_mem(ad.M_ST_P1_AD, b'\x01')
        r_mem(ad.M_ST_P2_AD, b'\x01')

    elif cfg.b_m_st_p1.raw == b'\x01':
        r_mem(ad.M_ST_P1_AD, b'\x00')
        r_mem(ad.M_ST_P2_AD, b'\x00')

    r_mem(ad.M_GAUGE_P1_AD, b'\x10\x27')
    r_mem(ad.M_GAUGE_P2_AD, b'\x10\x27')


def MAX_Damage_ini():

    r_mem(ad.MAX_Damage_Pointer_AD, cfg.temp)

    addres = b_unpack(cfg.temp)
    addres = addres + 0x1c
    r_mem(addres, b'\x00\x00\x00\x00')
    r_mem(addres + 4, b'\x00\x00\x00\x00')


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
    else:
        cfg.anten = 0

    # if cfg.reset_flag == 1:
    #     cfg.Bar_flag = 0

    # バー追加処理
    if cfg.Bar_flag == 1:
        if (cfg.p1.hitstop == 0 or cfg.p2.hitstop == 0):
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

    BC_white = "\x1b[40m"
    FC_white = "\x1b[30m"

    WHITE = '\x1b[39m'
    RED = '\x1b[31m'

    atk = "\x1b[41m" + FC_DEF
    mot = "\x1b[107m" + FC_DEF
    grd = "\x1b[48;5;08m" + FC_DEF
    nog = "\x1b[38;5;243m" + BC_DEF
    fre = "\x1b[38;5;234m" + BC_DEF

    p1num = ""
    p2num = ""
    P1_b_c = ""
    P2_b_c = ""
    bc = ""
    fc = ""
    fb = ""
    # 1P
    if cfg.p1.atk != 0:  # 攻撃判定を出しているとき
        fb = atk

    elif cfg.p1.motion != 0:  # モーション途中
        fb = mot

    # elif cfg.noguard_p1 != 77:  # 硬直中
    #     fb = mot

    elif cfg.p1.hit != 0:  # ガード硬直中
        fb = grd

    elif cfg.p1.motion_type != 0:  # ガードできないとき
        fb = nog

    elif cfg.p1.motion == 0:  # 何もしていないとき
        fb = fre

    P1_b_c = fb

    # 2P
    if cfg.b_atk_p2.raw != b'\x00\x00\x00\x00':  # 攻撃判定を出しているとき
        fb = atk

    elif cfg.p2.motion != 0:  # モーション途中
        fb = mot

    elif cfg.p2.hit != 0:  # ガード硬直中
        fb = grd

    elif cfg.p2.motion_type != 0:  # ガードできないとき
        fb = nog

    elif cfg.p2.motion == 0:  # 何もしていないとき
        fb = fre

    P2_b_c = fbｓ

    if cfg.p1.motion != 0:
        p1num = str(cfg.p1.motion)
    else:
        p1num = str(cfg.p1.motion_type)

    if cfg.p2.motion != 0:
        p2num = str(cfg.p2.motion)
    else:
        p2num = str(cfg.p2.motion_type)

    if cfg.p1.hit != 0:
        p1num = str(cfg.p1.hit)

    if cfg.p2.hit != 0:
        p2num = str(cfg.p2.hit)

    if p1num == '0' and cfg.DataFlag1 == 1:
        P1_b_c = DEF + "\x1b[39m"
        p1num = str(abs(cfg.yuuriF))

    if p2num == '0' and cfg.DataFlag1 == 1:
        P2_b_c = DEF + "\x1b[39m"
        p2num = str(abs(cfg.yuuriF))

    if cfg.anten <= 1:
        cfg.Bar_num += 1
        if cfg.Bar_num == 80:
            cfg.Bar_num = 0
            cfg.Bar80_flag = 1

    cfg.p1_barlist[cfg.Bar_num] = P1_b_c + p1num.rjust(2, " ")[-2:]
    cfg.p2_barlist[cfg.Bar_num] = P2_b_c + p2num.rjust(2, " ")[-2:]


def bar_ini():
    cfg.reset_flag = 1
    cfg.P1_Bar = ""
    cfg.P2_Bar = ""
    cfg.Bar_num = 0
    cfg.interval = 0
    cfg.interval2 = 0
    cfg.bar_ini_flag2 = 0
    cfg.Bar80_flag = 0
    cfg.p1_index = 0
    cfg.p2_index = 0
    cfg.interval_time = 80

    for n in range(len(cfg.p1_barlist)):
        cfg.p1_barlist[n] = ""

    for n in range(len(cfg.p2_barlist)):
        cfg.p2_barlist[n] = ""


def firstActive_calc():
    # 計測開始の確認
    if cfg.p2.hitstop != 0 and cfg.act_flag_P1 == 0 and cfg.p1.hit == 0:
        cfg.p1.act = cfg.p1.zen
        cfg.act_flag_P1 = 1

    if cfg.p1.hitstop != 0 and cfg.act_flag_P2 == 0 and cfg.p2.hit == 0:
        cfg.p2.act = cfg.p2.zen
        cfg.act_flag_P2 = 1

    if cfg.p1.motion == 0 and cfg.p1.atk == 0:
        cfg.act_flag_P1 = 0

    if cfg.p2.motion == 0 and cfg.p2.atk == 0:
        cfg.act_flag_P2 = 0


def b_unpack(d_obj):
    num = 0
    num = len(d_obj)
    if num == 1:
        return unpack('b', d_obj.raw)[0]
    elif num == 2:
        return unpack('h', d_obj.raw)[0]
    elif num == 4:
        return unpack('l', d_obj.raw)[0]


def get_values():
    negligible_number = [0, 10, 11, 12,
                         13, 14, 15, 18,
                         20, 16, 594, 17]

    for n in cfg.P_info:
        n.x = b_unpack(n.b_x)
        if n.motion_type != 0:
            n.motion_type_old = n.motion_type
        n.motion_type = b_unpack(n.b_motion_type)

        n.motion = 256 - b_unpack(n.b_motion)
        n.atk = b_unpack(n.b_atk)
        n.inv = b_unpack(n.b_inv)

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
    state_str +=  END

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
        # debug_str_p1 = "f_timer " + str(cfg.f_timer).rjust(7, " ")
        # debug_str_p2 = "Bar_num " + str(cfg.Bar_num).rjust(7, " ")
        #
        # debug_str_p1 += "motion_type " + str(cfg.p1.motion_type).rjust(7, " ")
        # debug_str_p2 += "motion_type " + str(cfg.p2.motion_type).rjust(7, " ")
        # debug_str_p1 += " motion " + str(cfg.p1.motion).rjust(7, " ")
        # debug_str_p2 += " motion " + str(cfg.p2.motion).rjust(7, " ")
        # debug_str_p1 += " anten_stop " + str(cfg.p1.anten_stop).rjust(7, " ")
        # debug_str_p2 += " anten_stop " + str(cfg.p2.anten_stop).rjust(7, " ")
        # debug_str_p1 += " motion_chenge_flag " + str(cfg.p1.motion_chenge_flag).rjust(7, " ")
        # debug_str_p2 += " motion_chenge_flag " + str(cfg.p2.motion_chenge_flag).rjust(7, " ")
        # debug_str_p1 += " hitstop " + str(cfg.p1.hitstop).rjust(7, " ")
        # debug_str_p2 += " hitstop " + str(cfg.p2.hitstop).rjust(7, " ")
        # debug_str_p1 += " noguard " + str(cfg.p1.noguard).rjust(7, " ")
        # debug_str_p2 += " noguard " + str(cfg.p2.noguard).rjust(7, " ")
        # debug_str_p1 += " hitstop_old " + str(cfg.p1.hitstop_old).rjust(7, " ")
        # debug_str_p2 += " hitstop_old " + str(cfg.p2.hitstop_old).rjust(7, " ")
        #
        # debug_str_p1 += " anten " + str(cfg.anten).rjust(7, " ")

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


def timer_check():
    r_mem(ad.TIMER_AD, cfg.b_timer)
    cfg.f_timer = b_unpack(cfg.b_timer)
