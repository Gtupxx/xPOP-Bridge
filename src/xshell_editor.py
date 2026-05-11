import ctypes
import win32gui
from .utils import log, WM_GETTEXT, WM_GETTEXTLENGTH, XSHELL_TITLE_KEYWORD, SendMessage


class XshellEditor:
    """查找并操作 Xshell 撰写编辑框的辅助类。"""

    def __init__(self):
        self.hwnd = None

    def find(self):
        """定位 Xshell 的撰写 Edit 控件，找到则保存 `self.hwnd`."""
        if self.hwnd:
            try:
                if win32gui.IsWindow(self.hwnd):
                    return True
            except Exception:
                pass

        self.hwnd = None

        xshell_hwnd = None

        def enum_windows(hwnd, _):
            nonlocal xshell_hwnd
            title = win32gui.GetWindowText(hwnd)
            if XSHELL_TITLE_KEYWORD in title:
                xshell_hwnd = hwnd
                log.info(f"找到Xshell: {title}")
                return False
            return True

        win32gui.EnumWindows(enum_windows, None)

        if not xshell_hwnd:
            log.warning("未找到Xshell")
            return False

        write_panel = None

        def enum_child(hwnd, _):
            nonlocal write_panel
            cls = win32gui.GetClassName(hwnd)
            text = win32gui.GetWindowText(hwnd)
            log.debug(f"{hwnd} | {cls} | {text}")
            if cls.startswith("Afx:ControlBar") and "撰写" in text:
                write_panel = hwnd
                log.info(f"找到撰写面板: {hwnd}")
                return False
            return True

        win32gui.EnumChildWindows(xshell_hwnd, enum_child, None)

        if not write_panel:
            log.warning("未找到撰写面板")
            return False

        edits = []

        def enum_edit(hwnd, _):
            cls = win32gui.GetClassName(hwnd)
            text = win32gui.GetWindowText(hwnd)
            log.debug(f"撰写子控件: {hwnd} | {cls} | {text}")
            if cls == "Edit":
                edits.append(hwnd)
            return True

        win32gui.EnumChildWindows(write_panel, enum_edit, None)

        if not edits:
            log.warning("撰写面板中未找到Edit")
            return False

        self.hwnd = edits[0]
        log.info(f"使用撰写Edit: {self.hwnd}")
        return True

    def get_text(self):
        length = win32gui.SendMessage(self.hwnd, WM_GETTEXTLENGTH, 0, 0)
        buffer = ctypes.create_unicode_buffer(length + 1)
        SendMessage(self.hwnd, WM_GETTEXT, length + 1, ctypes.byref(buffer))
        return buffer.value

    def get_cursor(self):
        start = ctypes.c_uint()
        end = ctypes.c_uint()
        SendMessage(self.hwnd, 0x00B0, ctypes.byref(start), ctypes.byref(end))
        return start.value

    def set_cursor(self, pos):
        SendMessage(self.hwnd, 0x00B1, pos, pos)
