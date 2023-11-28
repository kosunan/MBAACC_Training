import os
import time
import psutil
import ctypes
import struct
from ctypes import wintypes
from struct import unpack

process_handle = 0
base_address = 0


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("th32ModuleID", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("GlblcntUsage", wintypes.DWORD),
        ("ProccntUsage", wintypes.DWORD),
        ("modBaseAddr", ctypes.POINTER(wintypes.BYTE)),
        ("modBaseSize", wintypes.DWORD),
        ("hModule", wintypes.HMODULE),
        ("szModule", ctypes.c_byte * 256),
        ("szExePath", ctypes.c_byte * 260),
    ]


def wait_process(process_name):
    global process_handle
    global base_address

    """
    指定されたプロセスが起動するまで待機する
    """
    while True:
        pid = get_pid(process_name)
        if pid:
            print(f"{process_name} is running (PID: {pid})")

            base_address = get_base_address(pid)
            process_handle = get_process_handle(pid)
            return
        else:
            os.system("cls")
            print(f"Waiting for {process_name} to start...")
            time.sleep(0.5)


def get_pid(process_name):
    """
    指定されたプロセス名のプロセスIDを取得する
    """
    dict_pids = {
        p.info["name"]: p.info["pid"]
        for p in psutil.process_iter(attrs=["name", "pid"])
    }
    try:
        pid = dict_pids[process_name]
    except KeyError:
        pid = False

    return pid


def get_process_handle(pid):
    global process_handle
    global base_address
    """
    指定されたプロセスのプロセスハンドルを取得する
    """
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
    return process_handle


def get_base_address(pid):
    """
    指定されたプロセスのベースアドレスを取得する
    """
    # MODULEENTRY32を取得
    snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x00000008, pid)
    lpme = MODULEENTRY32()
    lpme.dwSize = ctypes.sizeof(lpme)
    res = ctypes.windll.kernel32.Module32First(snapshot, ctypes.byref(lpme))
    while pid != lpme.th32ProcessID:
        res = ctypes.windll.kernel32.Module32Next(snapshot, ctypes.byref(lpme))
    b_baseAddr = ctypes.create_string_buffer(8)
    b_baseAddr.raw = lpme.modBaseAddr
    base_addr = unpack("q", b_baseAddr.raw)[0]
    return base_addr


def w_Mem(address, data, size):
    ctypes.windll.kernel32.WriteProcessMemory(
        process_handle,
        address,
        data,
        size,
        None,
    )


def r_Mem(address, size):
    buffer = ctypes.create_string_buffer(size)
    ctypes.windll.kernel32.ReadProcessMemory(
        process_handle,
        address,
        buffer,
        size,
        None,
    )
    return buffer.raw


class MemoryBlock:
    def __init__(self, address, size):
        self.address = address
        self.size = size
        self.int_data = 0
        self.data = ctypes.create_string_buffer(size)

    def write_memory(self, data=None):
        if data is not None:
            self.data = data
        w_Mem(base_address + self.address, self.data, self.size)

    def write_absolute(self, address, data=None):
        if data is not None:
            self.data = data
        w_Mem(address, self.data, self.size)

    def read_memory(self):
        raw_data = r_Mem(base_address + self.address, self.size)
        ctypes.memmove(self.data, raw_data, self.size)
        return self.decode_data()

    def read_absolute(self, address):
        raw_data = r_Mem(address, self.size)
        ctypes.memmove(self.data, raw_data, self.size)
        return self.decode_data()

    def decode_data(self):
        if self.size == 1:
            self.int_data = struct.unpack("b", self.data)[0]
        elif self.size == 2:
            self.int_data = struct.unpack("h", self.data)[0]
        elif self.size == 4:
            self.int_data = struct.unpack("i", self.data)[0]
        else:
            return "Invalid data size"

        return self.int_data
