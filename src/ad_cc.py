
import cfg_cc
cfg = cfg_cc
P_info = cfg.P_info

###########################################################################
# 各種アドレス
###########################################################################
TIMER_AD = 0x162A40

CAM1_X_AD = 0x164B14
CAM1_Y_AD = 0x15DEC4
CAM2_X_AD = 0x164B18
CAM2_Y_AD = 0x15DEC8

PLR_STRUCT_SIZE = 0xAFC  # 3084

DAT_P1_AD = 0x155140  # 1Pデータ開始位置
DAT_P2_AD = DAT_P1_AD + PLR_STRUCT_SIZE
DAT_P3_AD = DAT_P2_AD + PLR_STRUCT_SIZE
DAT_P4_AD = DAT_P3_AD + PLR_STRUCT_SIZE

RECORDING_MODE_AD = 0x155137
GAME_MODE_AD = 0x14EEE8
DUMMY_STATUS_AD = 0x34D7F8
# STATUS_STAND( 0 )STATUS_JUMP( 1 )#STATUS_CROUCH( 2 )
# STATUS_CPU( 3 )#STATUS_MANUAL( 4 )#STATUS_DUMMY( 5 )
#STATUS_RECORD( -1 )
ANTEN_STOP_AD = 0x162A48  # 全体停止

TRAINING_PAUSE_AD = 0x162A64  # メニュー画面開いているとき
MAX_DAMAGE_AD = 0x157E0C

OBJ_AD = 0x27BD70  # オブジェクトデータ開始位置
STOP_SITUATION_AD = 0x158600  # 停止状況データ開始位置


DAMAGE_AD = 0x157DD8  # ダメージアドレス開始位置
DAMAGE2_AD = 0x157E10  # ダメージアドレス開始位置

GAUGE_POSITION = 0x15DEF0

RESET_AD = 0x15DEC3  # リセット FF
SAVE_BASE_AD = 0x66A0E8
# SAVE_BASE_AD = 0x5634A0 + base_ad
SAVE_END_AD = 0x26A0E8
COMB_AFTER_TIMER_AD = 0x36E708

FN1_KEY_AD = 0x37144C  # BUTTON_FN1
FN2_KEY_AD = 0x37144D  # BUTTON_FN2 リセットキー



P_info[0].dmp_ad = DAT_P1_AD
P_info[1].dmp_ad = DAT_P1_AD + PLR_STRUCT_SIZE
P_info[2].dmp_ad = DAT_P1_AD + PLR_STRUCT_SIZE * 2
P_info[3].dmp_ad = DAT_P1_AD + PLR_STRUCT_SIZE * 3

P_info[0].motion_type_ad = DAT_P1_AD
P_info[1].motion_type_ad = DAT_P1_AD + PLR_STRUCT_SIZE
P_info[2].motion_type_ad = DAT_P1_AD + PLR_STRUCT_SIZE * 2
P_info[3].motion_type_ad = DAT_P1_AD + PLR_STRUCT_SIZE * 3

P_info[0].motion_ad = 0x157FC0
P_info[1].motion_ad = 0x1581CC
P_info[2].motion_ad = 0x157FC0
P_info[3].motion_ad = 0x1581CC

P_info[0].atk_ad = 0x155454
P_info[1].atk_ad = 0x155454 + PLR_STRUCT_SIZE
P_info[2].atk_ad = 0x155454 + PLR_STRUCT_SIZE * 2
P_info[3].atk_ad = 0x155454 + PLR_STRUCT_SIZE * 3

P_info[0].inv_ad = DAT_P1_AD
P_info[1].inv_ad = DAT_P1_AD
P_info[2].inv_ad = DAT_P1_AD
P_info[3].inv_ad = DAT_P1_AD

P_info[0].step_inv_ad = 0x1552B5
P_info[1].step_inv_ad = 0x1552B5 + PLR_STRUCT_SIZE
P_info[2].step_inv_ad = 0x1552B5 + PLR_STRUCT_SIZE * 2
P_info[3].step_inv_ad = 0x1552B5 + PLR_STRUCT_SIZE * 3

P_info[0].x_ad = DAT_P1_AD + 0xF8
P_info[1].x_ad = DAT_P1_AD + 0xF8 + PLR_STRUCT_SIZE
P_info[2].x_ad = DAT_P1_AD + 0xF8 + PLR_STRUCT_SIZE * 2
P_info[3].x_ad = DAT_P1_AD + 0xF8 + PLR_STRUCT_SIZE * 3

P_info[0].gauge_ad = 0x155210
P_info[1].gauge_ad = 0x155210 + PLR_STRUCT_SIZE
P_info[2].gauge_ad = 0x155210 + PLR_STRUCT_SIZE * 2
P_info[3].gauge_ad = 0x155210 + PLR_STRUCT_SIZE * 3

P_info[0].tag_flag_ad = 0x155302
P_info[1].tag_flag_ad = 0x155302 + PLR_STRUCT_SIZE
P_info[2].tag_flag_ad = 0x155302 + PLR_STRUCT_SIZE * 2
P_info[3].tag_flag_ad = 0x155302 + PLR_STRUCT_SIZE * 3

P_info[0].hitstop_ad = DAT_P1_AD + 0x162
P_info[1].hitstop_ad = DAT_P1_AD + 0x162 + PLR_STRUCT_SIZE
P_info[2].hitstop_ad = DAT_P1_AD + 0x162 + PLR_STRUCT_SIZE * 2
P_info[3].hitstop_ad = DAT_P1_AD + 0x162 + PLR_STRUCT_SIZE * 3

# P_info[0].seeld_ad = 0x27D150
# P_info[1].seeld_ad = 0x27D150 + PLR_STRUCT_SIZE
# P_info[2].seeld_ad = 0x27D150 + PLR_STRUCT_SIZE * 2
# P_info[3].seeld_ad = 0x27D150 + PLR_STRUCT_SIZE * 3

P_info[0].anten_stop_ad = 0x158908
P_info[1].anten_stop_ad = 0x158908 + PLR_STRUCT_SIZE
P_info[2].anten_stop_ad = 0x158908
P_info[3].anten_stop_ad = 0x158908 + PLR_STRUCT_SIZE

P_info[0].atk_st_ad_pointer_ad = 0x155450
P_info[1].atk_st_ad_pointer_ad = 0x155450 + PLR_STRUCT_SIZE
P_info[2].atk_st_ad_pointer_ad = 0x155450 + PLR_STRUCT_SIZE * 2
P_info[3].atk_st_ad_pointer_ad = 0x155450 + PLR_STRUCT_SIZE * 3
