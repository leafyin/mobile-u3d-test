# encoding=utf-8

import threading
import unittest
import platform
import subprocess

from example.ExampleTest import ExampleTest
from pywebio.output import *
from functools import partial

from airtest.core.api import *


class MainGUI:

    def __init__(self):
        # adb devices
        self.devices = []
        system = platform.system()
        if system == 'Windows':
            cmd = "..\\init.bat"
        elif system in ['Darwin', 'Linux']:
            cmd = "sh ../init.sh"
        else:
            return
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        stdout = process.stdout.readlines()
        # 去掉头部尾部
        try:
            stdout.pop(0)
            stdout.pop(len(stdout) - 1)
        except IndexError:
            print("device not found")
            return
        for i in range(len(stdout)):
            if ":" or "emulator" in stdout[i]:
                self.devices.append(stdout[i].split("device")[0].strip("\t"))
        print(f"{len(self.devices)} device have been found {self.devices}")

        def buttons(d):

            def onoff():
                connect_device(f"Android:///{d}?cap_method=javacap&touch_method=adb")
                keyevent("26")

            def _exec_():
                subprocess.Popen(f"python ..\\example\\ExampleTest.py {d}",
                                 stdout=subprocess.PIPE,
                                 shell=True,
                                 encoding='utf-8')
                toast(f"设备{d}执行用例")

            return put_buttons(["开关", "运行"], onclick=[onoff, _exec_])

        def table():
            li = []
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromTestCase(ExampleTest)
            for case in suite:
                k = [case]
                li.append(k)
            return put_table(li)

        def init_gui():
            # gui part
            ggui = []
            for d in self.devices:
                ts = [d, table(), buttons(d)]
                ggui.append(ts)
            return put_table(ggui, header=["设备", "用例", "操作"])

        put_button("运行所有已连接设备", onclick=lambda: toast("Clicked"))
        init_gui()


gui = MainGUI()
