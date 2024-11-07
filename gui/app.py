# encoding=utf-8

import json
import logging
import threading
import unittest
import platform
import subprocess
import Logging
import Base

from bottle import *

from airtest.core.api import *


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')


@route('/')
def index():
    return template('index')


@route('/show')
def show():
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
                deviceid = stdout_str[i].split("device")[0].strip("\t")
                auto_setup(devices=[
                    f"Android://127.0.0.1:5037/{deviceid}?cap_method=JAVACAP"
                    f"&&ori_method=MINICAPORI"
                    f"&&touch_method=MAXTOUCH"
                ])
                devices.append(deviceid)
        logging.info(f"{len(devices)} devices have been found {devices}")
    result = {
        'code': 2000,
        'devices': devices,
        'initMsg': '所有设备均已初始化'
    }
    return json.dumps(result)


@post('/selectedDevice')
def select_device():
    data = request.json
    logging.info(data)
    result = {
        'code': 2000
    }
    return json.dumps(result)


if __name__ == '__main__':
    run(host='localhost', port=9547, debug=True, reloader=True)
