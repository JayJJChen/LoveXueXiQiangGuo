import time

from utils.ghost import Ghost


class Bot(Ghost):
    def __init__(self, **kwargs):
        Ghost.__init__(self, **kwargs)

    def take_exam(self, weekly=False):
        """
        weekly: True to take weekly, else take daily
        """
        if weekly:
            self._to_weekly_exam()
        else:
            self._to_daily_exam()
        time.sleep(3)
        for _ in range(5):
            self._answer()
        self._submit()
        self.finger.back()

    def _to_daily_exam(self):
        """go to one daily exam"""
        self.to_main()
        self.to_exam_root()
        self.finger.tap(140, 1550)  # lazy coord

    def _to_weekly_exam(self):
        """find weekly exam"""
        self.to_main()
        self.to_exam_root()
        self._goto("more")
        self._find_weekly_exam()

    def _do_choice(self, c="A"):
        """c: str, which choice to choose"""
        self._goto(c)

    def _do_fill(self, image, s="1"):
        """s: str, which string to fill"""
        coords = self.eye.find(self._image_path("bracket"), multi_target=True, img=image)
        if not len(coords):
            input("Sorry, I can't find any blank to fill, help me! Hit Enter to continue")
        else:
            for x, y in coords:
                self.finger.tap(x, y)
                self.finger.input_number(s)  # todo: check if it's number or text
                self.finger.back()

    def _answer(self):
        """answer one question then continue"""
        img = self.eye.see()
        if self.eye.find(self._image_path("A"), img=img):
            self._do_choice("A")
        else:
            self._do_fill(img, "1")
        self._bottom_tab(4)

    def _submit(self):
        """confirm submit after last question is answered"""
        self._goto("submit")
