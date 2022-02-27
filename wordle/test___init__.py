from unittest import TestCase
import wordle as wdl
from wordle import return_score


def get_common_chars():
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
     'w', 'x', 'y', 'z']

    s = wdl.get_scores(chars, wdl.all_words)
    print({k: v for k, v in sorted(s.items(), key=lambda item: item[1])})


def return_possible_words():
    history = {"yellow": dict(), "grey": dict(), "green": dict(), "regex": set()}
    second_words, h = wdl.generate_new_word_list("pactsrhomb", "XXXXXXXXXX", wdl.answer_words, history)

    print(second_words, len(second_words))


def return_possible_words_answers():
    history = {"yellow": dict(), "grey": dict(), "green": dict(), "regex": set()}
    second_words, h = wdl.generate_new_word_list("scampberth", "XXXXXXXXXX", wdl.answer_words, history)

    print(second_words, len(second_words))



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

    def test_scoring(self):
        s = wdl.get_scores(wdl.all_words, wdl.all_words)
        print({k: v for k, v in sorted(s.items(), key=lambda item: item[1])})

    # find the best word which doesn't contain s,c,a,m or p
    def test_scoring_second(self):
        history = {"yellow": dict(), "grey": dict(), "green": dict(), "regex": set()}
        second_words, h = wdl.generate_new_word_list("caste", "XXXXX", wdl.answer_words, history)
        s = wdl.get_scores(second_words, wdl.all_words)
        print({k: v for k, v in sorted(s.items(), key=lambda item: item[1]) if v > 2000})


    def test_return_possible_words_answers(self):
        return_possible_words_answers()

    def test_return_possible_words(self):
        return_possible_words()

    def test_chars(self):
        get_common_chars()
