import re
import sys
import numpy as np


# this regex will allow strings with any characters in the same position as the input word to pass.
# it is used to try and "score" a word for it's
def generate_usability_regex(w):
    output = ""
    for i in range(len(w)):
        output += "^.{" + str(i) + "}[" + w[i] + "]|"
    return output[:-1]


def setup(a_w):
    print("processing the scores of each word across the entire population")
    all_scores = dict()
    for word in a_w:
        scoreRE = re.compile(generate_usability_regex(word))
        all_scores[word] = len(list(filter(scoreRE.match, a_w)))
    return all_scores


def generate_new_word_list(w, r, prev_word_list, h):
    zipped = tuple(zip(range(len(w)), w, r))
    print("zipped", zipped)
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
        print(rule)
        new_words = list(filter(rule.match, new_words))

    return new_words, h


def play_round(input_word, result, old_words, all_scores, prev_history):
    new_words, new_history = generate_new_word_list(input_word, result, old_words, prev_history)

    # redeclare scores after each pass.
    scores = dict()

    for word in new_words:
        scoreRE = re.compile(generate_usability_regex(word))
        scores[word] = len(list(filter(scoreRE.match, new_words))) * all_scores[word]

    print([(w, scores[w]) for w in new_words])
    return max(scores, key=scores.get), history


with open("resources/wordle_allowed.txt", 'rt') as nw:
    all_words = np.array([line.rstrip() for line in nw])

with open("resources/wordle_answers.txt", 'rt') as nw:
    answer_words = np.array([line.rstrip() for line in nw])

all_words = np.append(all_words, answer_words)
words = answer_words
result = ""

history = {"yellow": dict(), "grey": dict(), "green": dict()}

all_scores = setup(answer_words)

# ideal best word has been precalculated, it takes a long time to run over every word in the dictionary, so this speeds
# it up a bit
print("first word recommendation: sores")

while result != "GGGGG":
    input_word = input("Enter the word you input: ")
    result = input("Enter the result of inputting your first word (example: YGYXX) ")
    next_word, history = play_round(input_word, result, words, all_scores, history)
    print("next word recommendation: " + next_word)
