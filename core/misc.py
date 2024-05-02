import os
import sys

help_dict = ["help", "restart"]


def multi_line_input():
    """
    多行输入
    :return:
    """
    lines = []
    while True:
        line = input()
        if line == 'EOF':
            break
        elif line in help_dict:
            lines.append(line)
            break
        elif line == 'DROP':
            return "I'll drop it."
        lines.append(line)
    return '\n'.join(lines)


def print_centered(text):
    """
    打印分割线
    @param text: 居中文字
    @return:
    """
    try:
        terminal_width = os.get_terminal_size().columns
    except os.error:
        terminal_width = 20
    text_width = len(text)
    left_padding = (terminal_width - text_width - len(text)) // 2
    print('-' * left_padding + text + '-' * left_padding)


def signal_handler(sig, frame):
    print()
    print_centered("任务结束")
    sys.exit(0)
