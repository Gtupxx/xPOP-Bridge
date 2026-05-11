import time
import keyboard
import config
from src.controller import Controller
from src.utils import log


def main():
    """程序入口：注册快捷键并保持运行（死循环）。"""
    controller = Controller()

    # 使用配置中的快捷键
    # keyboard.add_hotkey(config.HOTKEY, controller.send_current_line)
    keyboard.add_hotkey(
        config.HOTKEY,
        controller.send_current_line,
        suppress=True
    )

    log.info("启动成功!")

    # 不再等待 ESC，改为死循环保持进程运行
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()