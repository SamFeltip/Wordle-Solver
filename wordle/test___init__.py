from unittest import TestCase
import wordle as wdl
from wordle import return_score

class Test(TestCase):
    def test_return_score(self):
        if return_score("beret", "grief") != "XXYGX":
            self.fail()

    def test_double_in_answer(self):
        if return_score("broil", "chill") != "XXXYG":
            self.fail()

    def test_double_in_query(self):
        # return_score("corer", "cower")
        print(wdl.auto_play_wordle("cower", "crane"))

