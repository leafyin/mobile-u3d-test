# encoding=utf-8
from abc import ABC

from airtest.core.api import *
from poco.exceptions import PocoNoSuchNodeException, PocoTargetTimeout

from Base import Base


class AndroidPocoBase(Base, ABC):

    def __init__(self, deviceid):
        super().__init__(deviceid)

    def click(self, name):
        self.poco(name).click()
        sleep(self.speed)

    def set_text(self, name, content):
        this = self.poco(name)
        this.click()
        this.set_text(content)
        sleep(self.speed)

    def find_on_horizontal(self, obj, target, length):
        """
        水平查找元素（水平滑动也就是横向滑动，跟垂直不一样，一般是局部位置横向滑动，所以需要一个元素的初始位置）
        :param obj: 对象名称
        :param target: 参照的对象名称
        :param length: 滑动步长
        :return: None
        """
        obj, target = self.poco(obj), self.poco(target)
        if not target.exists():
            return
        target_pos = target.get_position()
        start_pos = (target_pos[0] * self.width, target_pos[1] * self.height)
        end_pos = (target_pos[0] * self.width - length, target_pos[1] * self.height)
        while 1:
            if obj.exists():
                break
            swipe(start_pos, end_pos, duration=0.25, steps=60)

    def find_on_vertical(self, obj: str, length, top_target=None, end_target=None):
        """
        垂直查找元素
        duration&steps可以控制滑动的视觉流畅度，默认duration=0.25，steps=60
        :param obj: 对象名称
        :param length: 滑动步长，如果要查找的元素在当前页面过长建议设置头尾标签，top_target,end_target
        :param top_target: 头部标签，确定页面头部
        :param end_target: 尾部标签，确定页面尾部
        :return: None
        """
        def up():
            """
            向上滑动
            :return:
            """
            start_pos = (mid_x, mid_y + init_length)
            end_pos = (mid_x, mid_y - length)
            swipe(start_pos, end_pos, duration=0.25, steps=60)

        def down():
            """
            向下滑动
            :return:
            """
            start_pos = (mid_x, mid_y - init_length)
            end_pos = (mid_x, mid_y + length)
            swipe(start_pos, end_pos, duration=0.25, steps=60)

        # 屏幕的中心位置坐标
        mid_x = self.width / 2
        mid_y = self.height / 2
        init_length = 200
        obj = self.poco(obj)
        top_target = self.poco(top_target)
        end_target = self.poco(end_target)
        while 1:
            try:
                self.poco.wait_for_any([obj], timeout=2)
                # 调整偏移，定位到屏幕中间位置
                obj_pos = obj.get_position()
                obj_absolute_pos_y = obj_pos[1] * self.height
                if obj_absolute_pos_y < mid_y:
                    swipe((mid_x, mid_y), (mid_x, mid_y + (mid_y - obj_absolute_pos_y)), duration=0.25, steps=60)
                if obj_absolute_pos_y > mid_y:
                    swipe((mid_x, mid_y), (mid_x, mid_y - (obj_absolute_pos_y - mid_y)), duration=0.25, steps=60)
                return
            except PocoNoSuchNodeException as e:
                print(e.message)
            except PocoTargetTimeout as e:
                print(e.message)
            if top_target is not None and end_target is not None:
                swipe_flag = True
                if top_target.exists():
                    swipe_flag = True
                if end_target.exists():
                    swipe_flag = False
                if swipe_flag:
                    up()
                if not swipe_flag:
                    down()
            else:  # 没设置则按照默认滑动次数
                swipe_count = 0
                if swipe_count == 10:
                    swipe_count = 0
                if swipe_count < 5:
                    up()
                    swipe_count += 1
                if swipe_count > 5:
                    down()
                    swipe_count += 1


if __name__ == '__main__':
    p = AndroidPocoBase("10.1.0.163:5555", "")
    pass
