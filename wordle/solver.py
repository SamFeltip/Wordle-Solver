import numpy as np
import re

import wordle as wdl


def generate_new_word_list(w, r, prev_word_list, h):
    zipped = tuple(zip(range(len(w)), w, r))
    regex_list = list()

    for (i, c, s) in zipped:
        if s == "Y":
            if c not in h["green"]:
                if c not in h["yellow"]:
                    h["yellow"][c] = list()

                h["yellow"][c].append(i)

        if s == "G":
            h["green"][c] = i
            # remove any greens from yellow if they were added in this round
            if c in h["yellow"]:
                del h["yellow"][c]
        if s == "X":
            if c not in h["grey"]:
                h["grey"][c] = list()

            h["grey"][c].append(i)

    # create regex for green positions
    for c in h["green"].keys():
        regex_list.append(re.compile(
            "^(.{" + str(h["green"][c]) + "}[" + c + "])"
        ))

    # create regex for yellow positions
    for c in h["yellow"].keys():
        # the word must contain this char
        regex_list.append(re.compile(
            "^(.*[" + c + "].*)"
        ))

        # the word must not be in any previous positions
        for i in h["yellow"][c]:
            regex_list.append(re.compile(
                "^(?!.{" + str(i) + "}[" + c + "])"
            ))

    # create regex for grey positions (in case of duplicates)
    for c in h["grey"].keys():
        # the word must not be in any previous positions
        for i in h["grey"][c]:
            regex_list.append(re.compile(
                "^(?!.{" + str(i) + "}[" + c + "])"
            ))

    # second regex to exclude chars that aren't in the word (excluding those in yellow and green)
    regex_list.append(re.compile(
        "[^" + "".join([c for c in h["grey"].keys() if c not in h["yellow"] and c not in h["green"]]) + "]{" + str(len(w)) + "}"
    ))

    new_words = prev_word_list
    for rule in regex_list:
        new_words = list(filter(rule.match, new_words))

    return new_words, h


def play_round(input_word, result, old_words, prev_history):
    new_words, new_history = generate_new_word_list(input_word, result, old_words, prev_history)

    # redeclare scores after each pass.
    scores = dict()

    for word in new_words:
        scoreRE = re.compile(wdl.generate_usability_regex(word))
        scores[word] = len(list(filter(scoreRE.match, new_words))) * wdl.all_scores[word]

    return max(scores, key=scores.get), new_history


