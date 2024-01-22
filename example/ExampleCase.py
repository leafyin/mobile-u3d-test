# encoding=utf-8

from example.ExampleStep import *


class ExampleCase(ExampleStep):
    """
    测试用例
    """

    def __init__(self, deviceid):
        super().__init__(deviceid)

    def add_mood(self, mood, content=None):
        try:
            self.poco.wait_for_all(self.poco(DadaCard.MOOD_CARD_NO_DATA))
            self.click(mood)
            self.click(Mood.NOTE_REFRESH)
            if content is not None:
                self.set_text(Mood.NOTE_EDITOR, content=content)
            self.click(Mood.FINISH)
            assert_true(self.poco(Mood.MOOD_OK).exists(), "mood exists")
        except PocoNoSuchNodeException:
            assert_true(True, "已发表过心情")

    def mood_like(self):
        try:
            index = random.randint(0, 3)
            mood_select = self.poco(Mood.MOOD_SELECT)
            self.poco.wait_for_all(mood_select)
            this_mood = mood_select.child(Mood.MOOD_LIKE_LIST)[index]
            this_mood.click()
            # 再点击一次判断是否点上了
            this_mood.click()
            try:
                self.poco.wait_for_all(self.poco(Mood.MOOD_CANCEL))
            except PocoTargetTimeout:
                assert_false(False, "点赞不成功")
        except PocoNoSuchNodeException:
            assert_true(True, "还未发表过心情")

    def add_diet(self, name):
        self.locate_to_home_card([DadaCard.DIET_CARD_NO_DATA, DadaCard.DIET_CARD_DATA])
        try:
            diet_no_data = self.poco(DadaCard.DIET_CARD_NO_DATA)
            self.poco.wait_for_all(diet_no_data)
            diet_no_data.child(Button.ADD_BTN).click()
        except PocoNoSuchNodeException:
            self.poco(DadaCard.DIET_CARD_DATA).child(Button.ADD_DIET_BTN).click()
        self.choose_time(3)
        self.set_text(Edit.FOOD_NAME_EDIT, name)
        self.choose_pic()
        self.submit()

    def add_note(self, title, content):
        self.locate_to_home_card([DadaCard.NOTE_CARD_DATA, DadaCard.NOTE_CARD_DATA])
        try:
            note_no_data = self.poco(DadaCard.NOTE_CARD_NO_DATA)
            self.poco.wait_for_all(note_no_data)
            note_no_data.offspring(Button.ADD_BTN).click()
        except PocoNoSuchNodeException:
            self.poco(DadaCard.NOTE_CARD_DATA).child(Button.ADD_NOTE_BTN).click()
        self.set_text(Edit.TITLE_EDIT, title)
        self.set_text(Edit.NOTE_EDIT, content)
        self.choose_pic()
        self.submit()

    def add_med(self, name, dosage, use):
        self.locate_to_home_card([DadaCard.MED_CARD_NO_DATA, DadaCard.MED_CARD_DATA])
        try:
            med_no_data = self.poco(DadaCard.MED_CARD_NO_DATA)
            self.poco.wait_for_all(med_no_data)
            med_no_data.child(Button.ADD_BTN).click()
        except PocoNoSuchNodeException:
            self.poco(DadaCard.MED_CARD_DATA).child(Button.ADD_MED_BTN).click()
        self.choose_time(2)
        self.set_text(Edit.DRUG_NAME_EDIT, name)
        self.click(TextView.DOSAGE)
        self.set_text(Edit.DOSAGE_EDIT, content=dosage)
        self.click(TextView.CONFIRM)
        self.set_text(Edit.MEDICAL_USE_EDIT, content=use)
        self.choose_pic(number=1)
        self.submit()
