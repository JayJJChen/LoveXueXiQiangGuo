import os
import subprocess

import cv2
import numpy as np


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

    def see(self, refresh=True):
        """read phone screen image, capture if not exist"""
        img_path = os.path.join(self.temp_path, "temp.png")
        if not os.path.exists(img_path) or refresh:
            self._screen_shot()
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        return img

    def find(self, target_path, multi_target=False, threshold=0.95):
        """
        finds target center coord

        returns None if nothing found
        else returns [[x1, y1], [x2, y2], ...]
        """
        img = self.see()
        target = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)
        w_target, h_target = target.shape[::-1]  # shape of the target
        res = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
        if res.max() < threshold:
            return None

        coords = []
        max_val = 0
        loc = np.where(res >= threshold)
        for y, x in zip(*loc):
            if multi_target:
                coords.append([x + w_target // 2, y + h_target // 2])
            else:
                if res[y, x] > max_val:
                    max_val = res[y, x]
                    coords = [[x + w_target // 2, y + h_target // 2]]

        return coords
