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


def get_base_addres():
    cfg.pid = 0
    while cfg.pid == 0:
        dict_pids = pidget()
        try:
            cfg.pid = dict_pids["MBAA.exe"]
        except:
            os.system('cls')
            print("Waiting for MBAA to start")
            time.sleep(0.2)

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


def b_unpack(d_obj):
    num = 0
    num = len(d_obj)
    if num == 1:
        return unpack('b', d_obj.raw)[0]
    elif num == 2:
        return unpack('h', d_obj.raw)[0]
    elif num == 4:
        return unpack('l', d_obj.raw)[0]


def r_mem(ad, b_obj):
    ReadMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)
    return b_unpack(b_obj)


def r_mem_2(ad, b_obj):
    ReadMem(cfg.h_pro, ad, b_obj, len(b_obj), None)
    return b_unpack(b_obj)


def w_mem(ad, b_obj):
    WriteMem(cfg.h_pro, ad + cfg.base_ad, b_obj, len(b_obj), None)


def para_get(obj):
    obj.num = r_mem(obj.ad, obj.b_dat)


def para_get_2(obj):
    obj.num = r_mem_2(obj.ad, obj.b_dat)


def para_set(obj):
    w_mem(obj.ad, obj.b_dat)


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


def situationCheck():
    # 状況チェック
    para_get(cfg.fn1_key)
    para_get(cfg.fn2_key)
    para_get(cfg.dummy_st)
    para_get(cfg.recording_mode)
    para_get(cfg.stop)

    for n in cfg.P_info:
        if n.motion_type.num != 0:
            n.motion_type_old = n.motion_type.num
        para_get(n.motion_type)
        para_get(n.motion)
        para_get(n.x_posi)
        para_get(n.y_posi1)
        para_get(n.y_posi2)
        para_get(n.air_flag)
        para_get(n.circuit)
        para_get(n.atk)
        para_get(n.step_inv)
        para_get(n.seeld)
        para_get(n.tag_flag)
        para_get(n.anten_stop)
        para_get(n.hitstop)
        para_get(n.stop)
        n.hit.num = 0
        para_get(n.throw_inv)
        para_get(n.atk_st_pointer)
        n.atk_st.ad = n.atk_st_pointer.num + 0x42
        n.throw.ad = n.atk_st_pointer.num + 0x44
        para_get_2(n.atk_st)
        para_get_2(n.throw)

    tagCharacterCheck()


def tagCharacterCheck():

    if cfg.P1.tag_flag.num == 0:
        cfg.p_info[0] = cfg.p1 = cfg.P1
        cfg.p_info[2] = cfg.p3 = cfg.P3

    elif cfg.P1.tag_flag.num == 1:
        cfg.p_info[0] = cfg.p1 = cfg.P3
        cfg.p_info[2] = cfg.p3 = cfg.P1

    if cfg.P2.tag_flag.num == 0:
        cfg.p_info[1] = cfg.p2 = cfg.P2
        cfg.p_info[3] = cfg.p4 = cfg.P4

    elif cfg.P2.tag_flag.num == 1:
        cfg.p_info[1] = cfg.p2 = cfg.P4
        cfg.p_info[3] = cfg.p4 = cfg.P2


def situationMem():

    # 状況を記憶
    save.P_info = copy.deepcopy(cfg.P_info)

    for n in save.P_info:
        para_get(n.dmp)

    para_get(save.obj)
    para_get(save.stop_situation)
    para_get(save.stop)
    para_get(save.damage)
    para_get(save.damage2)
    para_get(save.cam1_x)
    para_get(save.cam2_x)
    para_get(save.cam1_y)
    para_get(save.cam2_y)


def situationWrit():
    # 状況を再現
    for n in save.P_info:
        para_set(n.dmp)

    para_set(save.obj)
    para_set(save.stop_situation)
    para_set(save.stop)
    para_set(save.damage)
    para_set(save.damage2)
    para_set(save.cam1_x)
    para_set(save.cam2_x)
    para_set(save.cam1_y)
    para_set(save.cam2_y)


def view_st():

    # 全体フレームの取得
    overall_calc()

    # 技の発生フレームの取得
    firstActive_calc()

    # 硬直差の取得
    advantage_calc()

    # キャラの状況推移表示
    if (cfg.p1.motion.num != 0 or cfg.p1.hitstop.num != 0 or cfg.p1.hit.num != 0 or
            cfg.p2.motion.num != 0 or cfg.p2.hitstop.num != 0 or cfg.p2.hit.num != 0):

        cfg.reset_flag = 0
        cfg.bar_flag = 1
        cfg.interval = 0
    else:
        cfg.bar_flag = 0
        cfg.interval += 1

    # バーリセット判定
    determineReset()

    # 表示管理　表示するものが無くても前回の表示からインターバルの間は無条件で表示する
    if cfg.interval_time >= cfg.interval and cfg.reset_flag == 0:
        cfg.bar_flag = 1

    if cfg.bar_flag == 1:

        stop_flame_calc()

        # 攻撃判定持続計算
        for n in cfg.p_info:
            if n.atk.num != 0 and cfg.anten == 0 and cfg.hitstop == 0:  # 攻撃判定を出しているとき
                n.active += 1
            elif n.atk.num == 0 and cfg.anten == 0 and cfg.hitstop <= 1:  # 攻撃判定を出してないとき
                n.active = 0

        if cfg.anten == 0 and cfg.hitstop <= 1:
            cfg.bar_num += 1
            if cfg.bar_num == cfg.bar_range:
                cfg.bar_num = 0
                cfg.Bar80_flag = 1

        # バー追加処理
        bar_add()


def firstActive_calc():

    # 計測開始の確認
    if cfg.p2.hitstop.num != 0 and cfg.p1.act_flag == 0 and cfg.p1.hit.num == 0:
        cfg.p1.act = cfg.p1.zen
        cfg.p1.act_flag = 1

    if cfg.p1.hitstop.num != 0 and cfg.p2.act_flag == 0 and cfg.p2.hit.num == 0:
        cfg.p2.act = cfg.p2.zen
        cfg.p2.act_flag = 1

    if cfg.p1.motion.num == 0 and cfg.p1.atk.num == 0:
        cfg.p1.act_flag = 0

    if cfg.p2.motion.num == 0 and cfg.p2.atk.num == 0:
        cfg.p2.act_flag = 0


def advantage_calc():
    if cfg.p1.hit.num == 0 and cfg.p2.hit.num == 0 and cfg.p1.motion.num == 0 and cfg.p2.motion.num == 0:
        cfg.DataFlag1 = 0

    if (cfg.p1.hit.num != 0 or cfg.p1.motion.num != 0) and (cfg.p2.hit.num != 0 or cfg.p2.motion.num != 0):
        cfg.DataFlag1 = 1
        cfg.advantage_f = 0

    if cfg.DataFlag1 == 1:

        # 有利フレーム検証
        if (cfg.p1.hit.num == 0 and cfg.p1.motion.num == 0) and (cfg.p2.hit.num != 0 or cfg.p2.motion.num != 0):
            cfg.advantage_f += 1

        # 不利フレーム検証
        if (cfg.p1.hit.num != 0 or cfg.p1.motion.num != 0) and (cfg.p2.hit.num == 0 and cfg.p2.motion.num == 0):
            cfg.advantage_f -= 1


def overall_calc():
    # 全体フレームの取得
    if cfg.p1.motion.num != 0:
        cfg.p1.zen = cfg.p1.motion.num

    if cfg.p2.motion.num != 0:
        cfg.p2.zen = cfg.p2.motion.num


def determineReset():
    bar_ini_flag = 0

    if cfg.Bar80_flag == 1:
        cfg.interval_time = 10

    # インターバル後の初期化
    if cfg.interval_time <= cfg.interval:
        cfg.bar_ini_flag2 = 1

    # 表示するときリセット
    if cfg.bar_ini_flag2 == 1 and cfg.bar_flag == 1:
        bar_ini_flag = 1

    # 即時リセット
    if bar_ini_flag == 1:
        bar_ini()


def stop_flame_calc():

    # 暗転判定処理
    if cfg.stop.num != 0:
        cfg.anten += 1
    elif cfg.p1.anten_stop.num != 0 or cfg.p2.anten_stop.num != 0:
        cfg.anten += 1
    else:
        cfg.anten = 0

    # ヒットストップ処理
    if (cfg.p1.hitstop.num != 0 and cfg.p2.hitstop.num != 0):
        cfg.hitstop += 1
    elif (cfg.p1.hitstop.num == 0 or cfg.p2.hitstop.num == 0):
        cfg.hitstop = 0


def text_font(rgb):
    Text_font_str = "\x1b[38;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return Text_font_str


def bg_font(rgb):
    bg_font_str = "\x1b[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m"
    return bg_font_str


def get_font(text_rgb, bg_rgb):
    return text_font(text_rgb) + bg_font(bg_rgb)


def bar_add():

    DEF = '\x1b[0m'
    FC_DEF = '\x1b[39m'
    BC_DEF = '\x1b[49m'

    atk = get_font((255, 255, 255), (255, 0, 0))
    mot = get_font((255, 255, 255), (65, 200, 0))
    grd_stun = get_font((255, 255, 255), (170, 170, 170))
    hit_stun = get_font((255, 255, 255), (170, 170, 170))
    fre = get_font((92, 92, 92), (0, 0, 0))
    jmp = get_font((177, 177, 177), (241, 224, 132))
    seeld = get_font((255, 255, 255), (145, 194, 255))
    inv = get_font((200, 200, 200), (255, 255, 255))
    inv_atk = get_font((255, 255, 255), (255, 160, 160))
    adv = get_font((255, 255, 255), (0, 0, 0))
    bunker = get_font((255, 255, 255), (225, 184, 0))
    bunker_atk = get_font((255, 255, 255), (225, 102, 0))
    air = get_font((125, 127, 168), (125, 127, 168))
    throw_number = [350]  # 投げやられ

    hit_number = [
        26,  # 立吹っ飛び
        29,  # 足払いやられ
        30,  # 垂直吹っ飛び
        354,  # 小バウンド
        900,  # 立やられ
        901,  # 立やられ
        902,  # 屈やられ
        903,  # やられ
        904,  # やられ
        905,  # 屈大やられ
        906,  # 立大やられ
        907,  # 立大やられ２
        908  # 屈大やられ2
    ]
    grd_number = [
        17,  # 屈ガード
        18,  # 立ガード
        19,  # 空中ガード
    ]

    ignore_number = [0, 10, 11, 12, 13, 14, 15, 20, 16, 594]

    jmp_number = [34, 35, 36, 37]

    for n in cfg.p_info:

        if n.motion.num != 0:
            num = str(n.motion.num)
            font = mot
            for list_a in jmp_number:  # ジャンプ移行中
                if n.motion_type.num == list_a:
                    font = jmp
                    break

            for list_a in hit_number:  # ヒット中
                if n.motion_type.num == list_a:
                    font = hit_stun
                    break

            for list_a in grd_number:  # ガード中
                if n.motion_type.num == list_a:
                    font = grd_stun
                    break

        elif n.motion.num == 0:
            num = str(n.motion_type.num)
            font = fre

            if cfg.DataFlag1 == 1:
                if n == cfg.p_info[0] or n == cfg.p_info[1]:
                    font = adv
                    num = str(abs(cfg.advantage_f))

        if n.motion_type.num == 350:  # 投げやられ
            font = hit_stun

        elif n.atk_st.num == 12:  # バンカー　or 相殺
            font = bunker

        elif (n.atk_st.num == 10) and n.atk.num == 0:  # シールド
            font = seeld

        elif n.atk_st.num == 1 or n.atk_st.num == 0 or n.step_inv.num != 0:  # 無敵中
            font = inv

        n.barlist_1[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF

        font = ""
        num = ""
        if n.air_flag.num == 0 and n.y_posi1.num == 0 and n.y_posi2.num == 0:  # 地上にいる場合
            num = ""
        elif n.air_flag.num == 150 or n.y_posi1.num != 0 or n.y_posi2.num != 0:  # 空中にいる場合:
            num = "^"

        if n.atk.num != 0:  # 攻撃判定を出しているとき
            font = atk
            num = str(n.active)
            if n.air_flag.num == 150 or n.y_posi1.num != 0 or n.y_posi2.num != 0:  # 空中にいる場合:
                font += "\x1b[4m"

        n.barlist_2[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF

        num = str(n.motion_type.num)
        n.barlist_3[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF

        num = str(n.rigid_f.num)
        n.barlist_4[cfg.bar_num] = font + num.rjust(2, " ")[-2:] + DEF


def bar_ini():
    cfg.reset_flag = 1

    for n in cfg.p_info:
        n.Bar_1 = ""
        n.Bar_2 = ""
        n.Bar_3 = ""
        n.Bar_4 = ""

    cfg.st_Bar = ""
    cfg.bar_num = 0
    cfg.interval = 0
    cfg.interval2 = 0
    cfg.bar_ini_flag2 = 0
    cfg.Bar80_flag = 0
    cfg.interval_time = 80

    for n in range(cfg.bar_range):
        for m in cfg.p_info:
            m.barlist_1[n] = ""
            m.barlist_2[n] = ""
            m.barlist_3[n] = ""
            m.barlist_4[n] = ""

        cfg.st_barlist[n] = ""


def view():
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    x_p1 = str(cfg.p1.x_posi.num).rjust(8, " ")
    x_p2 = str(cfg.p2.x_posi.num).rjust(8, " ")

    zen_P1 = str(cfg.p1.zen).rjust(3, " ")
    zen_P2 = str(cfg.p2.zen).rjust(3, " ")

    circuit_p1 = str('{:.02f}'.format(cfg.p1.circuit.num / 100)).rjust(7, " ")
    circuit_p2 = str('{:.02f}'.format(cfg.p2.circuit.num / 100)).rjust(7, " ")

    act_P1 = str(cfg.p1.act).rjust(3, " ")
    act_P2 = str(cfg.p2.act).rjust(3, " ")

    advantage_f = str(cfg.advantage_f).rjust(7, " ")

    kyori = cfg.p1.x_posi.num - cfg.p2.x_posi.num

    for n in cfg.p_info:
        n.Bar_1 = ""
        n.Bar_2 = ""
        n.Bar_3 = ""
        n.Bar_4 = ""

    cfg.st_Bar = ""

    temp = cfg.bar_num

    for n in range(cfg.bar_range):
        temp += 1
        if temp == cfg.bar_range:
            temp = 0

        for m in cfg.p_info:
            m.Bar_1 += m.barlist_1[temp]
            m.Bar_2 += m.barlist_2[temp]
            m.Bar_3 += m.barlist_3[temp]
            m.Bar_4 += m.barlist_4[temp]

        cfg.st_Bar += cfg.st_barlist[temp]

    if kyori < 0:
        kyori = kyori * -1
    kyori = kyori / (21845)
    kyori = str(kyori)[:5]

    state_str = '\x1b[1;1H' + '\x1b[?25l'

    state_str += f'1P|Position{x_p1}'
    state_str += f' FirstActive{act_P1}'
    state_str += f' Overall{zen_P1}'
    state_str += f' Circuit{circuit_p1}%'

    if keyboard.is_pressed("F1"):
        f1 = '  \x1b[007m' + '[F1]Reset' + '\x1b[0m'
    else:
        f1 = '  [F1]Reset'

    if keyboard.is_pressed("F2"):
        f2 = '  \x1b[007m' + '[F2]Save state' + '\x1b[0m'
    else:
        f2 = '  [F2]Save state'

    state_str += '   ' + f1 + f2 + END

    state_str += '2P|Position' + x_p2
    state_str += ' FirstActive' + act_P2
    state_str += ' Overall' + zen_P2
    state_str += ' Circuit' + circuit_p2 + '%'
    state_str += END

    state_str += '  |Advantage' + advantage_f
    state_str += '  Range ' + kyori + 'M' + END

    state_str += '  | 1 2 3 4 5 6 7 8 91011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162636465666768697071727374757677787980' + END
    state_str += '1P|' + cfg.p1.Bar_1 + END
    state_str += '  |' + cfg.p1.Bar_2 + END
    state_str += '2P|' + cfg.p2.Bar_1 + END
    state_str += '  |' + cfg.p2.Bar_2 + END

    if cfg.debug_flag == 1:
        state_str = degug_view(state_str)

    print(state_str)


def degug_view(state_str):
    END = '\x1b[0m' + '\x1b[49m' + '\x1b[K' + '\x1b[1E'
    # os.system('mode con: cols=166 lines=15')
    debug_str_p1 = "f_timer " + str(cfg.f_timer).rjust(7, " ")
    debug_str_p2 = "bar_num " + str(cfg.bar_num).rjust(7, " ")

    debug_str_p1 += "motion_type " + str(cfg.p1.motion_type.num).rjust(7, " ")
    debug_str_p2 += "motion_type " + str(cfg.p2.motion_type.num).rjust(7, " ")
    debug_str_p1 += " motion " + str(cfg.p1.motion.num).rjust(7, " ")
    debug_str_p2 += " motion " + str(cfg.p2.motion.num).rjust(7, " ")
    debug_str_p1 += " anten_stop " + str(cfg.p1.anten_stop.num).rjust(7, " ")
    debug_str_p2 += " anten_stop " + str(cfg.p2.anten_stop.num).rjust(7, " ")
    debug_str_p1 += " hitstop " + str(cfg.p1.hitstop.num).rjust(7, " ")
    debug_str_p2 += " hitstop " + str(cfg.p2.hitstop.num).rjust(7, " ")
    debug_str_p1 += " anten " + str(cfg.anten).rjust(7, " ")
    debug_str_p1 += " stop " + str(cfg.stop.num).rjust(7, " ")
    debug_str_p1 += " y_posi " + str(cfg.p1.y_posi1.num).rjust(7, " ")
    debug_str_p1 += " y_posi " + str(cfg.p2.y_posi1.num).rjust(7, " ")
    debug_str_p1 += " y_posi " + str(cfg.p1.y_posi2.num).rjust(7, " ")
    debug_str_p1 += " y_posi " + str(cfg.p2.y_posi2.num).rjust(7, " ")
    debug_str_p1 += " tag_flag " + str(cfg.p1.tag_flag.num).rjust(7, " ")
    debug_str_p1 += " tag_flag " + str(cfg.p2.tag_flag.num).rjust(7, " ")

    # debug_str_p2 += " interval " + str(cfg.interval).rjust(7, " ")
    # debug_str_p2 += " Bar80_flag " + str(cfg.Bar80_flag).rjust(7, " ")
    # debug_str_p1 += "anten_stop.ad " + str(cfg.P_info[0].motion_type.ad).rjust(7, " ")

    state_str += debug_str_p1 + END
    state_str += debug_str_p2 + END
    # state_str += '1P|' + cfg.p1.Bar_2 + END
    state_str += '1P|' + cfg.p1.Bar_3 + END
    state_str += '1P|' + cfg.p1.Bar_4 + END

    return state_str


def situationReset():

    # 状況をリセット
    w_mem(ad.RESET_AD, b'\xff')


def pause():

    # 一時停止
    w_mem(ad.ANTEN_STOP_AD, b'\xff')


def play():

    # 再生
    w_mem(ad.ANTEN_STOP_AD, b'\x00')


def mode_check():
    para_get(cfg.game_mode)


def timer_check():
    cfg.f_timer = r_mem(ad.TIMER_AD, cfg.b_timer)


def MAX_Damage_ini():
    w_mem(ad.MAX_DAMAGE_AD, b'\x00\x00\x00\x00')


def disable_fn1():
    disable_fn1_1_AD = 0x0041F654
    disable_fn1_2_AD = 0x0041F652

    WriteMem(cfg.h_pro, disable_fn1_1_AD, b'\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90', 12, None)
    WriteMem(cfg.h_pro, disable_fn1_2_AD, b'\x90\x90', 2, None)
