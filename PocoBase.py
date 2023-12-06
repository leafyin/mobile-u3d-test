# encoding=utf-8
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException, PocoTargetTimeout

from Base import Base


class PocoBase(Base):

    def __init__(self, deviceid, logdir, packagename):
        super().__init__(deviceid, logdir)
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

    def click(self, name):
        self.poco(name).click()
        sleep(self.speed)

    def set_text(self, name, content=""):
        this = self.poco(name)
        this.click()
        this.set_text(content)
        sleep(self.speed)
        pass

    def find(self, obj, direction=True, length=300):
        """
        查找控件并定位到中间位置
        duration&steps可以控制滑动的视觉流畅度，默认duration=0.25，steps=60
        :param obj: 可以是一个控件也可以是一堆控件
        :param direction: 滑动方向
        :param length: 滑动步长
        :return: None
        """
        # 屏幕的中心位置
        mid_x = self.width / 2
        mid_y = self.height / 2
        init_length = 200
        swipe_count = 0
        break_count = 0
        objs = []
        while 1:
            if break_count == 50:
                break
            if direction:
                try:
                    for o in obj:
                        objs.append(self.poco(o))
                    self.poco.wait_for_any(objs, timeout=2)
                    swipe((mid_x, mid_y + init_length), (mid_x, mid_y - init_length), duration=0.25, steps=60)
                    return
                except PocoNoSuchNodeException as e:
                    print(e.message)
                except PocoTargetTimeout as e:
                    print(e.message)
                if swipe_count <= 10:
                    start_pos = (mid_x, mid_y + init_length)
                    end_pos = (mid_x, mid_y - length)
                    swipe(start_pos, end_pos, duration=0.25, steps=60)
                    swipe_count += 1
                if swipe_count >= 10:
                    start_pos = (mid_x, mid_y - init_length)
                    end_pos = (mid_x, mid_y + length)
                    swipe(start_pos, end_pos, duration=0.25, steps=60)
                    swipe_count += 1
                break_count += 1
            else:
                pass

