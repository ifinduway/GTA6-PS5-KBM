"""Show which HID device sends mouse (default) or keyboard input, via Windows Raw Input.
Usage: python find-input-device.py [seconds] [keyboard]
"""
import ctypes, ctypes.wintypes as wt, sys, time, collections

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
WM_INPUT = 0x00FF
RID_INPUT = 0x10000003
RIDI_DEVICENAME = 0x20000007
RIDEV_INPUTSINK = 0x00000100
RIM_TYPEMOUSE = 0

WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM)
user32.DefWindowProcW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]
user32.DefWindowProcW.restype = ctypes.c_ssize_t
user32.GetRawInputDeviceInfoW.argtypes = [wt.HANDLE, wt.UINT, wt.LPVOID, ctypes.POINTER(wt.UINT)]
user32.GetRawInputData.argtypes = [wt.HANDLE, wt.UINT, wt.LPVOID, ctypes.POINTER(wt.UINT), wt.UINT]

class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [("usUsagePage", wt.USHORT), ("usUsage", wt.USHORT), ("dwFlags", wt.DWORD), ("hwndTarget", wt.HWND)]

class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [("dwType", wt.DWORD), ("dwSize", wt.DWORD), ("hDevice", wt.HANDLE), ("wParam", wt.WPARAM)]

class WNDCLASSW(ctypes.Structure):
    _fields_ = [("style", wt.UINT), ("lpfnWndProc", WNDPROC), ("cbClsExtra", ctypes.c_int), ("cbWndExtra", ctypes.c_int),
                ("hInstance", wt.HINSTANCE), ("hIcon", wt.HICON), ("hCursor", wt.HANDLE), ("hbrBackground", wt.HBRUSH),
                ("lpszMenuName", wt.LPCWSTR), ("lpszClassName", wt.LPCWSTR)]

counts = collections.Counter()
names = {}

def device_name(h):
    if h not in names:
        size = wt.UINT(0)
        user32.GetRawInputDeviceInfoW(h, RIDI_DEVICENAME, None, ctypes.byref(size))
        buf = ctypes.create_unicode_buffer(size.value + 1)
        user32.GetRawInputDeviceInfoW(h, RIDI_DEVICENAME, buf, ctypes.byref(size))
        names[h] = buf.value or f"<handle {h}>"
    return names[h]

def wndproc(hwnd, msg, wparam, lparam):
    if msg == WM_INPUT:
        size = wt.UINT(0)
        user32.GetRawInputData(wt.HANDLE(lparam), RID_INPUT, None, ctypes.byref(size), ctypes.sizeof(RAWINPUTHEADER))
        buf = ctypes.create_string_buffer(size.value)
        if user32.GetRawInputData(wt.HANDLE(lparam), RID_INPUT, buf, ctypes.byref(size), ctypes.sizeof(RAWINPUTHEADER)) > 0:
            hdr = RAWINPUTHEADER.from_buffer_copy(buf)
            if hdr.dwType == WANT_TYPE:
                counts[device_name(hdr.hDevice) if hdr.hDevice else "<synthetic / no device>"] += 1
    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

def main(seconds):
    proc = WNDPROC(wndproc)
    wc = WNDCLASSW(lpfnWndProc=proc, lpszClassName="RawMouseProbe", hInstance=kernel32.GetModuleHandleW(None))
    user32.RegisterClassW(ctypes.byref(wc))
    user32.CreateWindowExW.argtypes = [wt.DWORD, wt.LPCWSTR, wt.LPCWSTR, wt.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                       ctypes.c_int, wt.HWND, wt.HMENU, wt.HINSTANCE, wt.LPVOID]
    user32.CreateWindowExW.restype = wt.HWND
    hwnd = user32.CreateWindowExW(0, "RawMouseProbe", "probe", 0, 0, 0, 0, 0, wt.HWND(-3), None, wc.hInstance, None)
    rid = RAWINPUTDEVICE(0x01, 0x06 if WANT_TYPE == 1 else 0x02, RIDEV_INPUTSINK, hwnd)
    if not user32.RegisterRawInputDevices(ctypes.byref(rid), 1, ctypes.sizeof(rid)):
        print("RegisterRawInputDevices failed", ctypes.GetLastError()); return
    msg = wt.MSG()
    end = time.time() + seconds
    while time.time() < end:
        while user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
            user32.TranslateMessage(ctypes.byref(msg)); user32.DispatchMessageW(ctypes.byref(msg))
        time.sleep(0.005)
    if not counts:
        print("no input seen - move the mouse or press keys while it runs")
    for name, n in counts.most_common():
        print(f"{n:6d}  {name}")

if __name__ == "__main__":
    WANT_TYPE = 1 if (len(sys.argv) > 2 and sys.argv[2] == "keyboard") else RIM_TYPEMOUSE
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 25)
