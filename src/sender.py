import time
import win32gui
import win32con
import win32api

import config

from .utils import log

WM_SETTEXT = 0x000C
VK_RETURN = 0x0D


class Sender:

    # 缓存输入框句柄
    hwnd = None

    @staticmethod
    def find_terminal_input():

        # hwnd仍然有效
        if Sender.hwnd:

            try:

                if win32gui.IsWindow(Sender.hwnd):

                    return Sender.hwnd

            except:
                pass

        log.info("开始查找NsComboBox")

        result = []

        def enum_windows(hwnd, _):

            title = win32gui.GetWindowText(hwnd)

            if "Xshell 8" in title:

                log.info(f"找到Xshell: {title}")

                def enum_child(child, __):

                    cls = win32gui.GetClassName(child)

                    # 只打印NsComboBox
                    if cls == "NsComboBox":

                        text = win32gui.GetWindowText(child)

                        log.info(f"找到NsComboBox: " f"{child} | {text}")

                        if text == '':
                            # 撰写栏的text为空，链接栏text不为空
                            result.append(child)

                    return True

                win32gui.EnumChildWindows(hwnd, enum_child, None)

            return True

        win32gui.EnumWindows(enum_windows, None)

        if not result:

            log.error("未找到NsComboBox")

            return None

        # 缓存句柄
        Sender.hwnd = result[-1]

        log.info(f"使用NsComboBox: {Sender.hwnd}")

        return Sender.hwnd

    @staticmethod
    def send(cmd):

        hwnd = Sender.find_terminal_input()

        if not hwnd:

            return

        log.info(f"发送命令: {cmd}")

        # 写入文本
        win32gui.SendMessage(hwnd, WM_SETTEXT, 0, cmd)

        time.sleep(config.SEND_DELAY)

        # 回车
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, VK_RETURN, 0)
