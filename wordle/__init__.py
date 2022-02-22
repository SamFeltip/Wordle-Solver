import numpy as np
import re
import random


# this regex will allow strings with any characters in the same position as the input word to pass.
# it is used to try and "score" a word for it's
def generate_usability_regex(w):
    output = ""
    for i in range(len(w)):
        output += "^.{" + str(i) + "}[" + w[i] + "]|"
    return output[:-1]


def get_scores():
    print("processing...")
    all_scores = dict()
    for word in answer_words:
        scoreRE = re.compile(generate_usability_regex(word))
        all_scores[word] = len(list(filter(scoreRE.match, all_words)))

    return all_scores


#
# test
#


def return_score(guess, answer):
    repeat_count = {c: answer.count(c) for c in answer}
    output = list()

    for i in range(len(answer)):
        if guess[i] == answer[i]:
            output.append('G')
            repeat_count[guess[i]] -= 1
        else:
            output.append('X')

    for i in range(len(answer)):
        if guess[i] in answer and repeat_count[guess[i]] > 0:
            output[i] = 'Y'
            repeat_count[guess[i]] -= 1
    return "".join(output)


def auto_play_wordle(answer, all_scores):
    words = answer_words
    result = ""

    history = {"yellow": dict(), "grey": dict(), "green": dict()}

    # ideal best word has been precalculated, it takes a long time to run over every word in the dictionary, so
    # this speeds it up a bit

    turns = 0
    guess_word = "sores"
    while result != "GGGGG":
        print(guess_word, " (", answer, ")")
        result = return_score(guess_word, answer)
        guess_word, history = play_round(guess_word, result, words, history, all_scores)
        turns += 1

    return turns


def test_solver(turns):
    all_scores = get_scores()
    total = 0
    for i in range(turns):
        answer = answer_words[random.randint(0, len(answer_words))]
        turns_taken = auto_play_wordle(answer, all_scores)
        print("answer: ", answer, ". turns taken: ", turns_taken)
        total += turns_taken

    return total / turns

#
# solver functions
#


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


def play_round(input_word, result, old_words, prev_history, all_scores):
    new_words, new_history = generate_new_word_list(input_word, result, old_words, prev_history)

    # redeclare scores after each pass.
    scores = dict()

    for word in new_words:
        scoreRE = re.compile(generate_usability_regex(word))
        scores[word] = len(list(filter(scoreRE.match, new_words))) * all_scores[word]

    return max(scores, key=scores.get), new_history


with open("../wordle/resources/wordle_allowed.txt", 'rt') as nw:
    all_words = np.array([line.rstrip() for line in nw])

with open("../wordle/resources/wordle_answers.txt", 'rt') as nw:
    answer_words = np.array([line.rstrip() for line in nw])

all_words = np.append(all_words, answer_words)



# tasty ( pasty )