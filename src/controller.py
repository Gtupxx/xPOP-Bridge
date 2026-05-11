from .xshell_editor import XshellEditor
from .line_manager import LineManager
from .sender import Sender
from .utils import log


class Controller:
    """主控制器：协调编辑器、行管理与发送器。"""

    def __init__(self):
        self.editor = XshellEditor()

    def send_current_line(self):
        try:
            if not self.editor.find():
                return

            text = self.editor.get_text()
            cursor = self.editor.get_cursor()

            line_index, line_text, start, end = LineManager.get_current_line(text, cursor)
            cmd = line_text.strip()

            log.info(f"当前行: {line_index + 1} | {repr(cmd)}")

            if cmd:
                Sender.send(cmd)

            next_cursor = LineManager.calc_next_cursor(text, line_index)
            self.editor.set_cursor(next_cursor)

        except Exception:
            log.exception("发送当前行失败")
