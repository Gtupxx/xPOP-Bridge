class LineManager:
    """处理文本行相关的纯函数集合。"""

    @staticmethod
    def get_current_line(text, cursor):

        lines = text.splitlines(True)

        # 空文本
        if not lines:
            return 0, "", 0, 0

        pos = 0

        for i, line in enumerate(lines):

            next_pos = pos + len(line)

            # 最后一行特殊处理
            if i == len(lines) - 1:

                if cursor <= next_pos:

                    return i, line, pos, next_pos

            else:

                if pos <= cursor < next_pos:

                    return i, line, pos, next_pos

            pos = next_pos

        # 光标超界时兜底返回最后一行
        last_index = len(lines) - 1
        last_line = lines[-1]

        start = len(text) - len(last_line)
        end = len(text)

        return last_index, last_line, start, end

    @staticmethod
    def calc_next_cursor(text, current_line):
        """计算下一次应设置的光标位置（循环回到首行）。"""
        lines = text.splitlines(True)
        if not lines:
            return 0
        next_line = current_line + 1
        if next_line >= len(lines):
            next_line = 0
        pos = 0
        for i in range(next_line):
            pos += len(lines[i])
        return pos
