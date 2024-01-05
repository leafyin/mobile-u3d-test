import sys
from AndroidBase import AndroidPocoBase
import unittest


class ExampleTest(unittest.TestCase):

    def setUp(self) -> None:
        self.ab = AndroidPocoBase("emulator-5554")
        pass

    def tearDown(self) -> None:
        pass

    def test_screen_toggle(self):
        self.ab.key_event(26)

    def test_physical_back(self):
        self.ab.key_event(4)


if __name__ == '__main__':
    unittest.main()
