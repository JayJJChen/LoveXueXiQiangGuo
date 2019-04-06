import subprocess
import time


class Finger:
    """basic class to simulate finger operations with adb commands"""

    def __init__(self, adb_path, sleep_sec=2):
        """
        adb_path: str, path to adb.exe
        sleep_sec: int, how many secs to wait after finger tap
        """
        self._adb_path = adb_path
        self._sleep_sec = sleep_sec

    def tap(self, x, y):
        cmd = "{} shell input tap {} {}"
        cmd = cmd.format(self._adb_path, x, y)
        subprocess.check_call(cmd)
        self._sleep()

    def swipe(self, x1, y1, x2, y2):
        cmd = "{} shell input swipe {} {} {} {}"
        cmd = cmd.format(self._adb_path, x1, y1, x2, y2)
        subprocess.check_call(cmd)
        self._sleep()

    def back(self):
        self._keycode("BACK")
        self._sleep()

    def home(self):
        self._keycode("HOME")
        self._sleep()

    def wake(self):
        self._keycode("WAKEUP")
        self._sleep()

    def enter(self):
        self._keycode("ENTER")
        self._sleep()

    def input_letter(self, text):
        """input English text only"""
        self._input(text)
        self._input("1")
        self._sleep()

    def input_number(self, number):
        """input numbers only"""
        self._input(str(number))
        self._sleep()

    def _input(self, text):
        for s in text:
            self._keycode(s.upper())
            time.sleep(0.1)

    def _keycode(self, x):
        """enter keycodes, reference:
        https://stackoverflow.com/questions/7789826/adb-shell-input-events"""
        cmd = "{} shell input keyevent KEYCODE_{}"
        cmd = cmd.format(self._adb_path, x)
        subprocess.check_call(cmd)

    def _sleep(self):
        time.sleep(self._sleep_sec)
