import os
import time

from utils.eye import Eye
from utils.finger import Finger


class Ghost:
    """class to navigate the app, with Eye and Finger"""

    def __init__(self, adb_path, temp_path, sleep_sec=2):
        self.eye = Eye(adb_path, temp_path)
        self.finger = Finger(adb_path, sleep_sec=sleep_sec)

    def to_main(self):
        """back to main page, doesn't support back from exam"""
        num_attempts = 0
        max_try = 10

        while not self._in_main():
            if self._in_exam():
                self._exit_exam()
            else:
                self.finger.back()
            num_attempts += 1
            if num_attempts >= max_try:  # failsafe
                input("I'm lost! Please help me go to main page! Hit Enter to continue")

    def to_score(self):
        """click the score from main page"""
        self._bottom_tab(2)
        self._goto("score")

    def to_exam_root(self):
        """go to the exam page root from main page"""
        self._bottom_tab(4)
        self._goto("exam_icon")

    def _exit_exam(self):
        """exit during exam to main"""
        self.finger.back()
        self._goto("exit_exam")
        self.finger.back()

    def swipe_up(self):
        self.finger.swipe(500, 1000, 500, 500)

    def swipe_down(self):
        self.finger.swipe(500, 500, 500, 1000)

    def _find_weekly_exam(self):
        """find available weekly exam in weekly exam page"""
        path = self._image_path("start_exam")
        coords = self.eye.find(path, multi_target=False)
        fail_count = 0
        while coords is None:
            # swipe up if there's no "start_exam"
            time.sleep(2)
            self.swipe_up()
            coords = self.eye.find(path, multi_target=False)
            if (fail_count > 10) and (coords is None):
                raise RuntimeError("I'm lost! Exiting!")
        self.finger.tap(*coords[0])

    def _goto(self, img_name):
        path = self._image_path(img_name)
        coords = self.eye.find(path, multi_target=False)
        fail_count = 0
        while coords is None:
            time.sleep(2)
            coords = self.eye.find(path, multi_target=False)
            if (fail_count > 5) and (coords is None):
                raise RuntimeError("I'm lost! Exiting!")
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

    def _in_exam(self):
        image = self.eye.see()
        in_exam = self.eye.find(self._image_path("in_exam"), img=image, multi_target=False)
        if in_exam is not None:
            return True
        else:
            return False

    def _in_main(self):
        image = self.eye.see()
        main_act = self.eye.find(self._image_path("main_act"), img=image, multi_target=False)
        main_inact = self.eye.find(self._image_path("main_inact"), img=image, multi_target=False)
        if (main_act is not None) or (main_inact is not None):
            return True
        else:
            return False

    @staticmethod
    def _image_path(img_name):
        path = os.path.join("images", "{}.png".format(img_name))
        return path
