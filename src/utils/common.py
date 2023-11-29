from ctypes import windll, wintypes, byref
import time

windll.winmm.timeBeginPeriod(1)  # タイマー精度を1msec単位にする


def high_precision_sleep(target_time):
    """
    指定された時間だけ高精度で待機します。
    """
    end_time = time.perf_counter() + target_time

    # 初期の待機（大部分の時間）
    initial_sleep_time = target_time - 0.002
    if initial_sleep_time > 0:
        time.sleep(initial_sleep_time)

    # 残りの時間をアクティブに待機
    while time.perf_counter() < end_time:
        pass


def high_precision_sleep_until(target_absolute_time):
    """
    Waits with high precision until the specified absolute time.

    Args:
    target_absolute_time (float): The absolute time at which to end the wait, based on the value returned by `time.perf_counter()`.
                                  The function waits until this time is reached. For example, `time.perf_counter() + 5` specifies a time 5 seconds from now.

    This function first uses `time.sleep` for efficient waiting during the initial part and then actively waits for the remaining very short duration to achieve higher precision.

    指定された絶対時刻まで高精度で待機します。

    引数:
    target_absolute_time (float): `time.perf_counter()`によって返される値を基準とした、待機を終了すべき絶対時刻。
                                  この時刻になるまで関数は待機します。例えば、`time.perf_counter() + 5`は現在から5秒後の時刻を指します。

    この関数は、初めの部分を`time.sleep`で効率よく待機し、最後のごく短い間はアクティブに待機することで、より高い精度での待機を実現します。
    """
    # Calculate the remaining time until the target absolute time
    remaining_time = target_absolute_time - time.perf_counter()

    if remaining_time > 0:
        # Initial wait for the major part of the time
        initial_sleep_time = remaining_time - 0.002
        if initial_sleep_time > 0:
            time.sleep(initial_sleep_time)

        # Actively wait for the remaining time
        while time.perf_counter() < target_absolute_time:
            pass


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


def changeFontSize(
    size_x, size_y
):  # Changes the font size to *size* pixels (kind of, but not really. You'll have to try it to chack if it works for your purpose ;) )
    from ctypes import POINTER, WinDLL, Structure, sizeof, byref
    from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(Structure):
        _fields_ = [
            ("X", SHORT),
            ("Y", SHORT),
        ]

    class CONSOLE_FONT_INFOEX(Structure):
        _fields_ = [
            ("cbSize", ULONG),
            ("nFont", DWORD),
            ("dwFontSize", COORD),
            ("FontFamily", UINT),
            ("FontWeight", UINT),
            ("FaceName", WCHAR * LF_FACESIZE),
        ]

    kernel32_dll = WinDLL("kernel32.dll")

    get_last_error_func = kernel32_dll.GetLastError
    get_last_error_func.argtypes = []
    get_last_error_func.restype = DWORD

    get_std_handle_func = kernel32_dll.GetStdHandle
    get_std_handle_func.argtypes = [DWORD]
    get_std_handle_func.restype = HANDLE

    get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
    get_current_console_font_ex_func.argtypes = [
        HANDLE,
        BOOL,
        POINTER(CONSOLE_FONT_INFOEX),
    ]
    get_current_console_font_ex_func.restype = BOOL

    set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
    set_current_console_font_ex_func.argtypes = [
        HANDLE,
        BOOL,
        POINTER(CONSOLE_FONT_INFOEX),
    ]
    set_current_console_font_ex_func.restype = BOOL

    stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = sizeof(CONSOLE_FONT_INFOEX)

    font.dwFontSize.X = size_x
    font.dwFontSize.Y = size_y

    set_current_console_font_ex_func(stdout, False, byref(font))


def text_font(rgb):
    return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def bg_font(rgb):
    return f"\x1b[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def get_font(text_rgb, bg_rgb):
    return text_font(text_rgb) + bg_font(bg_rgb)


def cmd_cursor_move(line, index):
    return "\x1b[" + str(line) + ";" + str(index) + "H"
