import os

from utils.eye import Eye
from utils.finger import Finger


class Navigator:
    """class to navigate the app, with Eye and Finger"""

    def __init__(self, adb_path, temp_path, sleep_sec=2):
        self.eye = Eye(adb_path, temp_path)
        self.finger = Finger(adb_path, sleep_sec=sleep_sec)

    def score_page(self):
        """click the score from main page"""
        self._bottom_tab(2)
        self._goto("score")

    def exam_page(self):
        """go to the exam page from main page"""
        self._bottom_tab(4)
        self._goto("exam_icon")

    def scroll_up(self):
        self.finger.swipe(500, 1000, 500, 500)

    def scroll_down(self):
        self.finger.swipe(500, 500, 500, 1000)

    def _goto(self, img_name):
        path = os.path.join("images", "{}.png".format(img_name))
        coords = self.eye.find(path, multi_target=False)
        self.finger.tap(*coords[0])

    def _bottom_tab(self, n):
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
