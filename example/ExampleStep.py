# encoding=ut-8
import random
from AndroidBase import *


class ExampleStep(AndroidPocoBase):
    """
    测试步骤类，封装单个、多个常用行为
    """

    def __init__(self, deviceid) -> None:
        super().__init__(deviceid)

    def more_btn(self):
        self.click(Button.MORE_BTN)

    def signup_btn(self):
        self.click(Button.SIGNUP_BTN)

    def more_login_btn(self):
        self.click(Button.LOGIN_BTN)

    def login_btn(self):
        self.click(Button.LOGIN)

    def add_device_btn(self):
        buttons = [Button.ADD_DEVICE_BTN, Button.ADD_DEVICE_BTN_1]
        for btn in buttons:
            if self.poco(btn).exists():
                self.click(btn)
                break

    def device_selector(self, deviceid):
        self.click(Button.DEVICE_NAME_BTN)
        self.permission_request()
        self.device_refresh()
        devices = self.poco(Device.DEVICE_LIST)
        for d in devices.child():
            de = d.child(Device.DEVICEID)
            print(de.get_text())
            if de.get_text() == deviceid:
                d.click()
                break

    def device_notification(self, event=True):
        try:
            notification = self.poco(Common.NOTIFICATION_WINDOW)
            self.poco.wait_for_all([notification], timeout=20)
            if event:
                self.click(Button.NOTIFICATION_AGREE_BTN)
            else:
                self.click(Button.NOTIFICATION_REFUSE_BTN)
        except PocoTargetTimeout:
            log("没人绑定这台设备")

    def device_for(self, for_who=1):
        if for_who:
            self.click(Device.ME_SELECT)
        else:
            self.click(Device.OTHER_SELECT)

    def device_refresh(self):
        self.click(Button.DEVICE_REFRESH)

    def get_verification_code_btn(self):
        self.click(Button.GET_VERIFICATION_CODE_BTN)

    def login_mode_switch(self):
        self.click(TextView.LOGIN_MODE_SWITCH)

    def agree_btn(self):
        self.click(Button.AGREE_BTN)

    def submit(self):
        self.click(Button.SUBMIT_BTN)

    def next_btn(self):
        self.click(Button.NEXT_BTN)

    def confirm_btn(self):
        self.click(Button.CONFIRM_BTN)

    def permission_request(self, is_allow=True):
        try:
            # 请求照片权限
            permission_icon = self.poco(Permission.PERMISSION_ICON)
            self.poco.wait_for_any([permission_icon], timeout=3)
            if is_allow:
                self.click(Permission.PERMISSION_ALLOW_BTN)
            else:
                self.click(Permission.PERMISSION_DENY_BTN)
        except PocoTargetTimeout:
            pass

    def choose_time(self, length):
        """
        时间选择
        :param: length 4或者3（diet是4，med是3）
        """
        try:
            index = random.randint(0, length)
            self.click(f"{APP_PREFIX}tv_time")
            self.poco(f"{APP_PREFIX}rv_time").child(f"{APP_PREFIX}ll_bg")[index].click()
        except PocoNoSuchNodeException:
            pass

    def choose_pic(self, number=4):
        """
        图片随机选择
        :param: number 选择图片的数量
        """
        try:
            # 生成一个随机数组，作于选择图片的顺序
            # 0下标是相机，所以从1开始
            random_arr = []
            if number <= 0:
                number = 1
            while 1:
                index = random.randint(1, number)
                if len(random_arr) == number:
                    break
                if index not in random_arr:
                    random_arr.append(index)
            print(f"the picture choose order is:{random_arr}")
            self.click(Common.PIC_CHOOSER)
            self.permission_request()
            try:
                pics = self.poco(RecyclerView.PIC_LIST)
                for i in random_arr:
                    pic = pics.child(Component.RELATIVE_LAYOUT)[i].child(f"{APP_PREFIX}tvCheck")
                    pic.click()
            except PocoNoSuchNodeException:
                self.poco(f"{APP_PREFIX}ps_iv_left_back").click()
            self.poco(Button.PIC_FINISH_BTN).click()
        except PocoNoSuchNodeException:
            pass

    def login(self, account, pwd):
        try:
            username = self.poco(TextView.USERNAME).get_text()
            if username not in ["Log In", "登录", "登入"]:
                return
            else:
                self.click(TextView.USERNAME)
                self.set_text(Edit.PHONE_NUMBER_EDIT, account)
                self.set_text(Edit.PASSWORD_EDIT, pwd)
                self.key_event(4)
                self.click(Button.AGREE_BTN)
                self.click(Button.LOGIN)
        except PocoNoSuchNodeException:
            assert_false(False, "login error")

    def find_add_member(self):
        caregivers = self.poco(RecyclerView.CAREGIVER_GROUP_LIST)
        if not caregivers.exists():
            return
        add_caregiver_btn = self.poco(Button.ADD_CAREGIVER_BTN)
        # 相对路径
        pos = caregivers.get_position()
        start_pos = (pos[0] * self.width, pos[1] * self.height)
        end_pos = (pos[0] * self.width - pos[0] * self.width / 2, pos[1] * self.height)
        while 1:
            if add_caregiver_btn.exists():
                break
            swipe(start_pos, end_pos, duration=0.25, steps=60)

    def add_member_btn(self):
        self.click(Button.ADD_CAREGIVER_BTN)

    def go_search_add_btn(self):
        self.click(Button.ADD_SEARCH_BTN)

    def search(self, number):
        self.set_text(Edit.SEARCH_CAREGIVER_EDIT, number)
        self.click(Button.SEARCH_BTN)

    def send_btn(self):
        self.click(Button.SEND_BTN)

    def setting_btn(self):
        self.click(Button.SETTING_BTN)

    def logout_btn(self):
        self.click(Button.LOGOUT_BTN)

    def message_btn(self):
        self.click(Button.MESSAGE_BTN)

    def caregiver_group_invitation_btn(self, btn_index):
        """

        :param btn_index:
        :return:
        """
        message_list = self.poco(Button.DATA_LIST)
        for i, m in enumerate(message_list.children()):
            if i == btn_index - 1:
                m.offspring(Button.CAREGIVER_GROUP_INVITATION_BTN).click()
                break

    async def upgrade_listener(self):
        while 1:
            upgrade_texts = ["Discover New Version"]
            try:
                if self.poco(TextView.UPGRADE_TITLE).get_text() in upgrade_texts:
                    self.click(ImageView.UPGRADE_CLOSE)
            except PocoNoSuchNodeException:
                pass
