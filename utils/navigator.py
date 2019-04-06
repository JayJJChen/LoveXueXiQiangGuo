import os

from utils.eye import Eye
from utils.finger import Finger


class Navigator:
    """class to navigate the app, with Eye and Finger"""

    def __init__(self, adb_path, temp_path, sleep_sec=2):
        self.eye = Eye(adb_path, temp_path)
        self.finger = Finger(adb_path, sleep_sec=sleep_sec)

    def bottom_tab(self, n):
        """
        navigate to bottom n_th tab, the screen resolution is 1080x1920

        args
        n: int, n_th bottom tab
        {
            n=0: 消息
            n=1: 关注
            n=2: 学刁
            n=3: 视频学习
            n=4: 我的
        }
        """
        x = [108 + 108 * 2 * i for i in range(5)]
        y = 1850
        self.finger.tap(x[n], y)

    def check_score(self):
        """click the score from main page"""
        path = os.path.join("images", "score.png")
        self.bottom_tab(2)
        coords = self.eye.find(path, multi_target=False)
        self.finger.tap(*coords[0])
