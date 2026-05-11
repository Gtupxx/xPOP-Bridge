# xPOP-Bridge

一个用于将 Xshell 撰写编辑区中逐行命令发送到终端的轻量 Python 插件。

## 特性
- 按行发送当前光标所在命令
- 支持配置快捷键与其他可定制项（见 `config.py`）

## 要求
- Windows（需要访问 Win32 API）
- Python 3.8+
- 依赖库：`pywin32`、`keyboard`

安装依赖：

```bash
pip install pywin32 keyboard
```

## 使用
1. 启动 Xshell 并打开要发送的撰写编辑区（Xshell 窗口标题中包含 `Xshell 8`）。
2. 在项目根目录运行：

```bash
python main.py
```

默认快捷键为 `f8`（可在 `config.py` 中修改）。程序以死循环保持运行，按 `Ctrl+C` 可退出。

## 配置
编辑项目根目录下的 `config.py` 来定制：

- `HOTKEY`：触发发送的快捷键（例如 `f8`）
- `XSHELL_TITLE_KEYWORD`：用于匹配 Xshell 窗口标题的关键字
- `SEND_DELAY`：发送命令后等待的秒数

## 注意
- 需要以能访问 GUI 的权限运行脚本（即在本地 Windows 环境）。
- 日志文件默认写入 `logs/date/xx-xx-xx.log`。
