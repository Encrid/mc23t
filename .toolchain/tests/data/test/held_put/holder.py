import os
import sys

path = sys.argv[1]
if os.name == 'nt':
    import ctypes
    from ctypes import wintypes as w

    k = ctypes.WinDLL('kernel32', use_last_error=True)
    k.CreateFileW.restype = w.HANDLE
    k.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, ctypes.c_void_p, w.DWORD, w.DWORD, w.HANDLE]
    k.ReadFile.argtypes = [w.HANDLE, ctypes.c_void_p, w.DWORD, ctypes.POINTER(w.DWORD), ctypes.c_void_p]
    k.CloseHandle.argtypes = [w.HANDLE]
    handle = k.CreateFileW(path, 0x80000000, 7, None, 3, 0, None)
    print('open', flush=True)
    sys.stdin.readline()
    bytes_of = ctypes.create_string_buffer(64)
    got = w.DWORD()
    k.ReadFile(handle, bytes_of, 64, ctypes.byref(got), None)
    k.CloseHandle(handle)
    held = bytes_of.raw[:got.value]
else:
    handle = os.open(path, os.O_RDONLY)
    print('open', flush=True)
    sys.stdin.readline()
    held = os.read(handle, 64)
    os.close(handle)
with open(path, 'rb') as now:
    print('held %s, now %s' % (held.decode().strip(), now.read().decode().strip()), flush=True)
