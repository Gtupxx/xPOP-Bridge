import ctypes
import logging

from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

import config

# 当前日期
TODAY = datetime.now().strftime("%Y-%m-%d")

# 当前时间
START_TIME = datetime.now().strftime("%H-%M-%S")

# 日志目录
LOG_DIR = Path(config.LOG_DIR) / TODAY

# 创建目录
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志文件
LOG_FILE = LOG_DIR / f"{START_TIME}.log"

# 日志格式
formatter = logging.Formatter(
    fmt=("%(asctime)s | " "%(levelname)-8s | " "%(message)s"), datefmt="%H:%M:%S"
)

# 文件日志
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1024 * 1024, backupCount=10, encoding="utf-8"
)

file_handler.setFormatter(formatter)

# 控制台日志
console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)

# root logger
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])

# logger
log = logging.getLogger("xshell-plugin")

# Win32 常量
EM_GETSEL = 0x00B0
EM_SETSEL = 0x00B1

WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E

# Xshell窗口关键字
XSHELL_TITLE_KEYWORD = config.XSHELL_TITLE_KEYWORD

# Win32 SendMessage
SendMessage = ctypes.windll.user32.SendMessageW
