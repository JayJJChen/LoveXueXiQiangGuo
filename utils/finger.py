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
        cmd = "{} shell input keyevent KEYCODE_BACK"
        cmd = cmd.format(self._adb_path)
        subprocess.check_call(cmd)
        self._sleep()

    def home(self):
        cmd = "{} shell input keyevent KEYCODE_HOME"
        cmd = cmd.format(self._adb_path)
        subprocess.check_call(cmd)
        self._sleep()

    def wake(self):
        cmd = "{} shell input keyevent KEYCODE_WAKEUP"
        cmd = cmd.format(self._adb_path)
        subprocess.check_call(cmd)
        self._sleep()

    def _sleep(self):
        time.sleep(self._sleep_sec)
