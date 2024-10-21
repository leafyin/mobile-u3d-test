# encoding=utf-8

import json
import threading
import unittest
import platform
import subprocess

from bottle import *

from airtest.core.api import *


@route('/')
def dropdown():
    response.content_type = 'application/json'
    devices = []
    system = platform.system()
    if system == 'Windows':
        cmd = "adb devices"
    elif system in ['Darwin', 'Linux']:
        cmd = "adb devices"
    else:
        return
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding='utf-8')
    # 处理子进程结束
    process.wait()
    # 确保文件关闭
    with process.stdout as stdout:
        stdout_str = stdout.readlines()
        # 去掉头部尾部
        stdout_str.pop(0)
        stdout_str.pop(len(stdout_str) - 1)
        for i in range(len(stdout_str)):
            if ":" or "emulator" in stdout_str[i]:
                devices.append(stdout_str[i].split("device")[0].strip("\t"))
        print(f"{len(devices)} devices have been found {devices}")
    return json.dumps(devices)


if __name__ == '__main__':
    run(host='localhost', port=9547, debug=True, reloader=True)
