from unittest import TestCase
from wordle.play import play_wordle


class Test(TestCase):
    def test_play_wordle(self):
        play_wordle("crain", 100)



#
# ['abled', 'alley']
# abled  ( alley )
