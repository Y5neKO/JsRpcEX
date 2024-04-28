import argparse
import json
import re
import signal

import requests
import pyperclip

from core.init_info import *
from core.banner import *
from core.color import *
from core.misc import *

help_info = """
执行模式说明:
Js数据支持多行输入,输入EOF结束
help: 帮助
restart: 重新监听(JsRpc部分功能需切换监听地址)
"""


def init():
    """
    获取需要注入的Js数据
    :return:
    """
    pyperclip.copy(injected_js)
    input("注入Js数据已复制,请直接粘贴在控制台执行,执行后回车")
    address_jsrpc = input("请输入JsRpc服务监听地址: ")
    pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$'
    if not bool(re.match(pattern, address_jsrpc)):
        print("格式有误,请重新输入")
        print_centered("任务结束")
        sys.exit(0)
    group = input("请输入组名: ")
    select_ID = input("是否携带ID连接通信(y/n): ")
    if select_ID == 'y':
        clientId = input("请输入客户端ID: ")
        url = demo.format(address_jsrpc, group).replace("hliang", clientId)
    elif select_ID == 'n':
        url = demo_ez.format(address_jsrpc, group)
    else:
        url = demo_ez.format(address_jsrpc, group)
        print("格式有误,默认选择n")
    select_TLS = input("是否使用TLS连接(y/n): ")
    if select_TLS == 'y':
        url = url.replace("ws://", "wss://")
    elif select_TLS == 'n':
        pass
    else:
        print("格式有误,默认选择n")
    pyperclip.copy(url)
    print("连接通信地址复制成功,请直接粘贴在控制台执行")


def execjs():
    """
    进入执行模式
    :return:
    """
    wsURL = input("请输入JsRpc服务监听地址: ")
    group = input("请输入组名: ")
    if not wsURL.startswith("http"):
        print("格式有误,请重新输入")
        execjs()
    else:
        print_centered("进入执行模式")
    print(help_info)

    while True:
        print(color("JsRpcEX@localhost:", "green") + "~" + color("$ ", "cyan"))
        js_code = multi_line_input()
        if js_code == 'restart':
            print_centered("任务重新开始")
            execjs()
        if js_code == 'help':
            print(help_info)
            continue
        data = {
            "group": group,
            "code": js_code
        }
        try:
            response = requests.post(wsURL, data=data)
        except requests.exceptions.ConnectionError:
            print("请求失败")
            return False
        res_json = json.loads(response.text)
        print(json.dumps(res_json, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    print(logo)
    parser = argparse.ArgumentParser(description="JsRpc执行器")
    parser.add_argument('--init', action='store_true', help='获取需要注入的Js数据')
    parser.add_argument("--execjs", action='store_true', help='进入执行模式')

    args = parser.parse_args()
    if len(sys.argv) > 1:
        print_centered("任务开始")
    if args.init:
        init()
    if args.execjs:
        execjs()
    if len(sys.argv) > 1:
        print_centered("任务结束")
