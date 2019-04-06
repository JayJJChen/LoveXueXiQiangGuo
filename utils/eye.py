import os
import subprocess

import cv2
from skimage.measure import regionprops, label


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

    def find(self, target_path, multi_target=False, threshold=0.95, img=None):
        """
        finds target center coord

        returns None if nothing found
        else returns [[x1, y1], [x2, y2], ...]
        """
        if img is None:
            img = self.see()
        target = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)
        w_target, h_target = target.shape[::-1]  # shape of the target
        heatmap = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
        heatmap_max = heatmap.max()
        if heatmap_max < threshold:
            return None
        if not multi_target:
            threshold = heatmap_max

        heatmap_labeled = label(heatmap >= threshold)
        heatmap_prop = regionprops(heatmap_labeled)

        coords = list()
        for prop in heatmap_prop:
            y, x = prop.centroid
            coords.append([int(x + w_target / 2), int(y + h_target / 2)])
            if not multi_target:
                return coords

        return coords
