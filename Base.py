# encoding=utf-8
import abc
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class Base:

    def __init__(self, deviceid, logdir="./report/"):
        auto_setup(devices=[
            f"Android://127.0.0.1:5037/{deviceid}?cap_method=JAVACAP"
            f"&&ori_method=MINICAPORI"
            f"&&touch_method=MAXTOUCH"
        ], logdir=logdir)
        self.poco = AndroidUiautomationPoco()
        self.device = self.poco.device
        self.width = self.device.display_info["width"]
        self.height = self.device.display_info["height"]
        self.speed = 1
        # 点亮屏幕
        if not self.device.is_screenon():
            self.poco.device.keyevent(keyname="26")

    @abc.abstractmethod
    def click(self, name):
        pass

    def key_event(self, keycode):
        """
        调用KeyEvent事件
        :param keycode:
        :return:
        """
        self.device.keyevent(str(keycode))
        sleep(self.speed)

    @abc.abstractmethod
    def set_text(self, name, content):
        pass

    @abc.abstractmethod
    def find_on_vertical(self, obj, length, top_target=None, end_target=None):
        pass

    @abc.abstractmethod
    def find_on_horizontal(self, obj, target, length):
        pass
