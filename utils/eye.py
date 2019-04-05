import subprocess
import numpy as np
import cv2
import os


class Eye:
    """basic class to read phone screen, black and white"""

    def __init__(self, adb_path, temp_path):
        self.adb_path = adb_path
        self.temp_path = temp_path
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

    def _screen_shot(self):
        """capture phone screen and store the image as temp_path/temp.png"""
        cmd = r"{} shell screencap -p /sdcard/screen.png"
        cmd = cmd.format(self.adb_path)
        subprocess.check_call(cmd)

        cmd = r"{} pull /sdcard/screen.png {}"
        cmd = cmd.format(self.adb_path, os.path.join(
            self.temp_path, "temp.png"))
        subprocess.check_call(cmd)

    def see(self):
        """read phone screen image, capture if not exist"""
        img_path = os.path.join(self.temp_path, "temp.png")
        if not os.path.exists(img_path):
            self._screen_shot()
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        return img
