from unittest import TestCase

from wordle import return_score


class Test(TestCase):
    def test_return_score(self):
        if return_score("beret", "grief") != "XXYGX":
            self.fail()
