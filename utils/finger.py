import subprocess
import time


class Finger:
    """basic class to simulate finger operations with adb commands"""

    def __init__(self, adb_path):
        self.adb_path = adb_path

    def tap(self, x, y):
        cmd = "{} shell input tap {} {}"
        cmd = cmd.format(self.adb_path, x, y)
        subprocess.check_call(cmd)

    def swipe(self, x1, y1, x2, y2):
        cmd = "{} shell input swipe {} {} {} {}"
        cmd = cmd.format(self.adb_path, x1, y1, x2, y2)
        subprocess.check_call(cmd)

    def back(self):
        cmd = "{} shell input keyevent KEYCODE_BACK"
        cmd = cmd.format(self.adb_path)
        subprocess.check_call(cmd)

    def home(self):
        cmd = "{} shell input keyevent KEYCODE_HOME"
        cmd = cmd.format(self.adb_path)
        subprocess.check_call(cmd)
