from ctypes import create_string_buffer
Bar80_flag = 0
bar_range = 80
cre = create_string_buffer

class para:
    def __init__(self, byte_len):
        self.ad = 0x00
        self.num = 0
        self.b_dat = create_string_buffer(byte_len)

class Character_info:
    def __init__(self):
        self.dmp = para(971)
        self.motion = para(4)
        self.motion_type = para(2)
        self.x_posi = para(4)
        self.y_posi1 = para(4)
        self.y_posi2 = para(4)
        self.air_flag = para(4)
        self.circuit = para(4)
        self.atk = para(4)
        self.atk_st_pointer = para(4)
        self.atk_st = para(1)
        self.inv = para(1)
        self.step_inv = para(1)
        self.seeld = para(1)
        self.tag_flag = para(1)
        self.anten_stop = para(1)
        self.anten_stop2 = para(4)
        self.hitstop = para(1)
        self.stop = para(1)

        self.hit = para(2)
        self.noguard = para(1)
        self.throw = para(4)
        self.throw_inv = para(1)
        self.rigid_f = para(1)

        self.motion_type_old = 0
        self.motion_chenge_flag = 0
        self.act = 0
        self.first_active = 0
        self.active = 0

        self.zen = 0
        self.act_flag = 0
        self.Bar_1 = ''
        self.Bar_2 = ''
        self.Bar_3 = ''
        self.Bar_4 = ''
        self.barlist_1 = list(range(bar_range))
        self.barlist_2 = list(range(bar_range))
        self.barlist_3 = list(range(bar_range))
        self.barlist_4 = list(range(bar_range))

P_info = [Character_info(), Character_info(), Character_info(), Character_info()]
p_info = [Character_info(), Character_info(), Character_info(), Character_info()]

for info1, info2 in zip(P_info, p_info):
    for n in range(bar_range):
        info1.barlist_1[n] = ""
        info1.barlist_2[n] = ""
        info1.barlist_3[n] = ""
        info1.barlist_4[n] = ""

        info2.barlist_1[n] = ""
        info2.barlist_2[n] = ""
        info2.barlist_3[n] = ""
        info2.barlist_4[n] = ""

pid = 0
h_pro = 0
base_ad = 0
f_timer = 0
b_timer = create_string_buffer(4)
f_timer2 = 0
fn1_key = para(1)
fn2_key = para(1)
dummy_st = para(1)
recording_mode = para(1)
stop = para(2)
game_mode = para(1)

P1 = P_info[0]
P2 = P_info[1]
P3 = P_info[2]
P4 = P_info[3]

p1 = p_info[0]
p2 = p_info[1]
p3 = p_info[2]
p4 = p_info[3]

st_barlist = list(range(bar_range))
for n in range(bar_range):
    st_barlist[n] = ""

bar_flag = 0
bar_num = 0
bar_ini_flag = 0
bar_ini_flag2 = 0
st_Bar = ""

DataFlag1 = 1
anten = 0
anten_flag = 0
advantage_f = 0
hitstop = 0
interval = 41
interval2 = 80
interval_time = 0
reset_flag = 0
temp = create_string_buffer(4)
debug_flag = 0
