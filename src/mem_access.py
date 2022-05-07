import psutil
import ctypes
from struct import unpack
import cfg_ml

wintypes = ctypes.wintypes
windll = ctypes.windll
sizeof = ctypes.sizeof
create_string_buffer = ctypes.create_string_buffer
byref = ctypes.byref

OpenProcess = windll.kernel32.OpenProcess
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
Module32First = windll.kernel32.Module32First
Module32Next = windll.kernel32.Module32Next


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

###########################################################################
# ベースアドレス取得
###########################################################################


dict_pids = {
    p.info["name"]: p.info["pid"]
    for p in psutil.process_iter(attrs=["name", "pid"])
}

cfg_ml.pid = dict_pids["MBAA.exe"]
cfg_ml.h_pro = OpenProcess(0x1F0FFF, False, cfg_ml.pid)

# MODULEENTRY32を取得
snapshot = CreateToolhelp32Snapshot(0x00000008, cfg_ml.pid)

lpme = MODULEENTRY32()
lpme.dwSize = sizeof(lpme)

res = Module32First(snapshot, byref(lpme))

while cfg_ml.pid != lpme.th32ProcessID:
    res = Module32Next(snapshot, byref(lpme))

b_baseAddr = create_string_buffer(8)
b_baseAddr.raw = lpme.modBaseAddr

base_ad = unpack('q', b_baseAddr.raw)[0]
b_anten_stop_p1 = create_string_buffer(1)
b_anten_stop_p2 = create_string_buffer(1)

b_atk_p1 = create_string_buffer(4)
b_atk_p2 = create_string_buffer(4)
b_cam = create_string_buffer(1500)
b_damage = create_string_buffer(4)
b_timer = create_string_buffer(4)
b_gauge_p1 = create_string_buffer(4)
b_gauge_p2 = create_string_buffer(4)
b_hit_p1 = create_string_buffer(2)
b_hit_p2 = create_string_buffer(2)
b_hitstop_p1 = create_string_buffer(4)
b_hitstop_p2 = create_string_buffer(4)
b_hosei = create_string_buffer(4)
b_m_st_p1 = create_string_buffer(1)
b_m_st_p2 = create_string_buffer(1)
b_mf_p1 = create_string_buffer(4)
b_mf_p2 = create_string_buffer(4)
b_mftp_p1 = create_string_buffer(2)
b_mftp_p2 = create_string_buffer(2)
b_noguard_p1 = create_string_buffer(1)
b_noguard_p2 = create_string_buffer(1)
b_tr_flag = create_string_buffer(4)

b_ukemi1 = create_string_buffer(2)
b_ukemi2 = create_string_buffer(2)

b_dat_p1 = create_string_buffer(4)
b_dat_p2 = create_string_buffer(4)
b_dat_p3 = create_string_buffer(4)
b_dat_p4 = create_string_buffer(4)

b_x_p1 = create_string_buffer(4)
b_x_p2 = create_string_buffer(4)
b_x_p3 = create_string_buffer(4)
b_x_p4 = create_string_buffer(4)

b_y_p1 = create_string_buffer(4)
b_y_p2 = create_string_buffer(4)
b_y_p3 = create_string_buffer(4)
b_y_p4 = create_string_buffer(4)

b_s_x_p1 = create_string_buffer(4)
b_s_x_p2 = create_string_buffer(4)
b_s_x_p3 = create_string_buffer(4)
b_s_x_p4 = create_string_buffer(4)

b_s_y_p1 = create_string_buffer(4)
b_s_y_p2 = create_string_buffer(4)
b_s_y_p3 = create_string_buffer(4)
b_s_y_p4 = create_string_buffer(4)

damage = create_string_buffer(4)
b_m_gauge_p1 = create_string_buffer(4)
b_m_gauge_p2 = create_string_buffer(4)
b_dmy_timer = create_string_buffer(4)
b_dmyend_timer = create_string_buffer(4)
b_hi_ko_flag_p1 = create_string_buffer(1)
b_hi_ko_flag_p2 = create_string_buffer(1)
b_start_posi = create_string_buffer(1)

temp = create_string_buffer(4)

###########################################################################
# 各種アドレス
###########################################################################

PLR_STRUCT_SIZE = 0xAFC  # 3084

DAT_P1_AD = 0x00555140  # 1Pデータ開始位置
DAT_P2_AD = DAT_P1_AD + PLR_STRUCT_SIZE  # 2Pデータ開始位置
DAT_P3_AD = DAT_P2_AD + PLR_STRUCT_SIZE  # 2Pデータ開始位置
DAT_P4_AD = DAT_P3_AD + PLR_STRUCT_SIZE  # 2Pデータ開始位置

# ST_AD = 0x0155C150  # 状況データ開始位置 6032
# STOP_ST_AD = 0x0059B390  # 停止状況データ開始位置

X_P1_AD = DAT_P1_AD + 0xF8
X_P2_AD = X_P1_AD + PLR_STRUCT_SIZE
X_P3_AD = X_P2_AD + PLR_STRUCT_SIZE
X_P4_AD = X_P3_AD + PLR_STRUCT_SIZE

ATK_P1_AD = DAT_P1_AD + 0x314
ATK_P2_AD = ATK_P1_AD + PLR_STRUCT_SIZE

MOTION_TYPE_P1_AD = DAT_P1_AD
MOTION_TYPE_P2_AD = MOTION_TYPE_P1_AD + PLR_STRUCT_SIZE

MOTION_P1_AD = 0x00557FC0
MOTION_P2_AD = 0x005581CC

HITSTOP_P1_AD = DAT_P1_AD + 0x162
HITSTOP_P2_AD = HITSTOP_P1_AD + PLR_STRUCT_SIZE

# HIT_P1_AD = DAT_P1_AD + 0x2D8
# HIT_P2_AD = HIT_P1_AD + PLR_STRUCT_SIZE

ANTEN_STOP_AD = DAT_P1_AD + 0x731
ANTEN2_STOP_AD = ANTEN_STOP_AD + PLR_STRUCT_SIZE

# HI_KO_P1_AD = DAT_P1_AD + 0x2A2
# HI_KO_P2_AD = HI_KO_P1_AD + PLR_STRUCT_SIZE

# UKEMI1_P1_AD = DAT_P1_AD + 0x2DC  # のけぞり時間
# UKEMI1_P2_AD = UKEMI1_P1_AD + PLR_STRUCT_SIZE

# UKEMI2_P1_AD = DAT_P1_AD + 0x2E4  # 受け身不能時間
# UKEMI2_P2_AD = UKEMI2_P1_AD + PLR_STRUCT_SIZE

# START_POSI_AD = 0x6EB888 + base_ad

# TR_FLAG_AD = 0x69A1E4 + base_ad

# DAMAGE_AD = 0x6D0940 + base_ad
CAM1_X_AD = 0x00564B14
CAM1_Y_AD = 0x0055DEC4
CAM2_X_AD = 0x00564B18
CAM2_Y_AD = 0x0055DEC8

STOP_AD = 0x6E6EB8 + base_ad

DAMAGE_AD = 0x00557DD8  # ダメージアドレス開始位置
DAMAGE2_AD = 0x00557E10  # ダメージアドレス開始位置

MAX_Damage = 0x00557E0C

TIMER_AD = 0x00562A40

RECORDING_MODE_ADDR = 0x00555137
DUMMY_STATUS_ADDR = 0x0074D7F8
#STATUS_STAND       ( 0 )
#STATUS_JUMP        ( 1 )
#STATUS_CROUCH      ( 2 )
#STATUS_CPU         ( 3 )
#STATUS_MANUAL      ( 4 )
#STATUS_DUMMY       ( 5 )
#STATUS_RECORD      ( -1 )
GAUGE_POSITION = 0x0055DEF0
PAUSE_AD = 0x00562A64
RESET_ADDR = 0x0055DEC3  # リセット FF
SAVE_BASE_AD = 0x66A0E8 + base_ad
# SAVE_BASE_AD = 0x5634A0 + base_ad
SAVE_END_AD = 0x66B6DF + base_ad
comb_aft_timer = 0x0076E708



def situationCheck():
    # タッグキャラ対策
    tagCharacterCheck()
    ReadMem(cfg.h_pro, ad.X_P1_AD + cfg.size_p1, cfg.b_x_p1, 4, None)
    ReadMem(cfg.h_pro, ad.ATK_P1_AD + cfg.size_p1, cfg.b_atk_p1, 4, None)
    ReadMem(cfg.h_pro, ad.HITSTOP_P1_AD + cfg.size_p1, cfg.b_hitstop_p1, 4, None)
    ReadMem(cfg.h_pro, ad.HIT_P1_AD + cfg.size_p1, cfg.b_hit_p1, 2, None)
    ReadMem(cfg.h_pro, ad.NOGUARD_P1_AD + cfg.size_p1, cfg.b_noguard_p1, 1, None)
    ReadMem(cfg.h_pro, ad.MOTION_TYPE_P1_AD + cfg.size_p1, cfg.b_mftp_p1, 2, None)
    ReadMem(cfg.h_pro, ad.MOTION_P1_AD + cfg.size_p1, cfg.b_mf_p1, 4, None)
    ReadMem(cfg.h_pro, ad.GAUGE_P1_AD + cfg.size_p1, cfg.b_gauge_p1, 4, None)
    ReadMem(cfg.h_pro, ad.ANTEN_STOP_AD + cfg.size_p1, cfg.b_anten_stop_p1, 1, None)
    ReadMem(cfg.h_pro, ad.M_GAUGE_P1_AD + cfg.size_p1, cfg.b_m_gauge_p1, 4, None)
    ReadMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, cfg.b_m_st_p1, 1, None)

    ReadMem(cfg.h_pro, ad.X_P2_AD + cfg.size_p2, cfg.b_x_p2, 4, None)
    ReadMem(cfg.h_pro, ad.ATK_P2_AD + cfg.size_p2, cfg.b_atk_p2, 4, None)
    ReadMem(cfg.h_pro, ad.HIT_P2_AD + cfg.size_p2, cfg.b_hit_p2, 2, None)
    ReadMem(cfg.h_pro, ad.HITSTOP_P2_AD + cfg.size_p2, cfg.b_hitstop_p2, 4, None)
    ReadMem(cfg.h_pro, ad.NOGUARD_P2_AD + cfg.size_p2, cfg.b_noguard_p2, 1, None)
    ReadMem(cfg.h_pro, ad.MOTION_TYPE_P2_AD + cfg.size_p2, cfg.b_mftp_p2, 2, None)
    ReadMem(cfg.h_pro, ad.MOTION_P2_AD + cfg.size_p2, cfg.b_mf_p2, 4, None)
    ReadMem(cfg.h_pro, ad.ANTEN2_STOP_AD + cfg.size_p2, cfg.b_anten_stop_p2, 1, None)
    ReadMem(cfg.h_pro, ad.GAUGE_P2_AD + cfg.size_p2, cfg.b_gauge_p2, 4, None)
    ReadMem(cfg.h_pro, ad.M_GAUGE_P2_AD + cfg.size_p2, cfg.b_m_gauge_p2, 4, None)
    ReadMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, cfg.b_m_st_p2, 1, None)

    ReadMem(cfg.h_pro, ad.UKEMI2_P2_AD + cfg.size_p2, cfg.b_ukemi1, 2, None)

    # 状況チェック
    ReadMem(cfg.h_pro, ad.TIMER_AD, cfg.b_timer, 4, None)
    ReadMem(cfg.h_pro, ad.HOSEI_AD, cfg.b_hosei, 4, None)
    ReadMem(cfg.h_pro, ad.UKEMI_AD, cfg.b_ukemi2, 2, None)

    ReadMem(cfg.h_pro, ad.DAMAGE_AD, cfg.b_damage, 4, None)
    ReadMem(cfg.h_pro, ad.START_POSI_AD, cfg.b_start_posi, 1, None)


def situationMem():
    # 状況を記憶
    # situationWrit
    ReadMem(cfg.h_pro, ad.CAM_AD, cfg.b_cam, 1500, None)
    ReadMem(cfg.h_pro, ad.X_P1_AD, save.x_p1, 4, None)
    ReadMem(cfg.h_pro, ad.X_P2_AD, save.x_p2, 4, None)
    ReadMem(cfg.h_pro, ad.X_P3_AD, save.x_p3, 4, None)
    ReadMem(cfg.h_pro, ad.X_P4_AD, save.x_p4, 4, None)

    ReadMem(cfg.h_pro, ad.M_GAUGE_P1_AD + cfg.size_p1, save.m_gauge_p1, 4, None)
    ReadMem(cfg.h_pro, ad.M_GAUGE_P2_AD + cfg.size_p2, save.m_gauge_p2, 4, None)

    ReadMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, save.m_st_p1, 1, None)
    ReadMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, save.m_st_p2, 1, None)

    # situationWrit2
    ReadMem(cfg.h_pro, ad.SAVE_BASE_AD, save.save_data, save.data_size2, None)
    ReadMem(cfg.h_pro, ad.DAT_P1_AD, save.P1_data1, save.data_size, None)
    ReadMem(cfg.h_pro, ad.DAT_P2_AD, save.P2_data1, save.data_size, None)


def situationWrit():
    # 状況を再現
    WriteMem(cfg.h_pro, ad.CAM_AD, cfg.b_cam, 1500, None)
    WriteMem(cfg.h_pro, ad.X_P1_AD, save.x_p1, 4, None)
    WriteMem(cfg.h_pro, ad.X_P2_AD, save.x_p2, 4, None)
    WriteMem(cfg.h_pro, ad.X_P3_AD, save.x_p3, 4, None)
    WriteMem(cfg.h_pro, ad.X_P4_AD, save.x_p4, 4, None)

    WriteMem(cfg.h_pro, ad.M_GAUGE_P1_AD + cfg.size_p1, save.m_gauge_p1, 4, None)
    WriteMem(cfg.h_pro, ad.M_GAUGE_P2_AD + cfg.size_p2, save.m_gauge_p2, 4, None)

    WriteMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, save.m_st_p1, 1, None)
    WriteMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, save.m_st_p2, 1, None)


def situationWrit2():
    # 状況を再現
    WriteMem(cfg.h_pro, ad.SAVE_BASE_AD, save.save_data, save.data_size2, None)
    WriteMem(cfg.h_pro, ad.DAT_P1_AD, save.P1_data1, save.data_size, None)
    WriteMem(cfg.h_pro, ad.DAT_P2_AD, save.P2_data1, save.data_size, None)


def moon_change():

    if cfg.b_m_st_p1.raw == b'\x00':
        WriteMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, b'\x01', 1, None)
        WriteMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, b'\x01', 1, None)

    elif cfg.b_m_st_p1.raw == b'\x01':
        WriteMem(cfg.h_pro, ad.M_ST_P1_AD + cfg.size_p1, b'\x00', 1, None)
        WriteMem(cfg.h_pro, ad.M_ST_P2_AD + cfg.size_p2, b'\x00', 1, None)

    WriteMem(cfg.h_pro, ad.M_GAUGE_P1_AD + cfg.size_p1, b'\x10\x27', 2, None)
    WriteMem(cfg.h_pro, ad.M_GAUGE_P2_AD + cfg.size_p2, b'\x10\x27', 2, None)


def MAX_Damage_ini():

    ReadMem(cfg.h_pro, ad.MAX_Damage_Pointer_AD, cfg.temp, 4, None)

    addres = unpack('l', cfg.temp.raw)[0]
    addres = addres + 0x1c
    WriteMem(cfg.h_pro, addres, b'\x00\x00\x00\x00', 4, None)
    WriteMem(cfg.h_pro, addres + 4, b'\x00\x00\x00\x00', 4, None)
