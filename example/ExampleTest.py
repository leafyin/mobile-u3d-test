import unittest

import HtmlTestRunner
from ExampleCase import *


class ExampleTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.this = ExampleCase(DEFAULT_DEVICE)
        start_app(PACKAGE_NAME)
        sleep(3)

    def tearDown(self) -> None:
        super().tearDown()
        report_name = f"/report/{self.id()}_{str(round(time.time() * 1000))}.html"
        simple_report(__file__, True, output=report_name)

    def doCleanups(self) -> None:
        super().doCleanups()
        del self
        stop_app(PACKAGE_NAME)
        stop_app(POCO_SERVICE_NAME)
        stop_app(POCO_SERVICE_TEST_NAME)
        sleep(3)

    def test_add_mood(self):
        self.this.add_mood(Mood.NOT_SURE)

    def test_mood_like(self):
        self.this.mood_like()

    def test_add_diet(self):
        self.this.add_diet("随便吃点")

    def test_add_note(self):
        self.this.add_note("好日子", "一起去遛狗吧！")

    def test_add_med(self):
        self.this.add_med("该吃药了", 15, "对身体好")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ExampleTest)
    runner = HtmlTestRunner.HTMLTestRunner(
        report_name=str(round(time.time()) * 1000),
        report_title="***自动化测试",
        open_in_browser=True,
        verbosity=2,
        buffer=True,
        resultclass=HtmlTestRunner.runner.HtmlTestResult
    )
    runner.run(suite)
