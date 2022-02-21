import re
import sys
import numpy as np

yellow = dict()
gray = ""
green = dict()


# this function adds one list onto the end of another, because .extend() wasn't working for me.
def extend(list1, list2):
    for i in list2:
        list1.append(i)
    return list1


# this regex will allow strings with any characters in the same position as the input word to pass.
# it is used to try and "score" a word for it's
def generate_usability_regex(w):
    output = ""
    for i in range(len(w)):
        output += "^.{" + str(i) + "}[" + w[i] + "]|"
    return output[:-1]


def generate_new_word_list(w, r, prev_word_list, ye, gy, gn):
    zipped = tuple(zip(range(len(w)), w, r))
    print("zipped", zipped)
    regex_list = list()

    for (i, c, s) in zipped:
        if s == "Y":
            if c not in gn:
                if c not in ye:
                    ye[c] = list()
                ye[c].append(i)
        if s == "G":
            gn[c] = i
            # remove any greens from yellow if they were added in this round
            if c in ye:
                del ye[c]
        if s == "X":
            if s not in gy:
                gy += c

    # create regex for green positions
    for c in gn.keys():
        regex_list.append(re.compile(
                "^(.{" + str(gn[c]) + "}[" + c + "])"
        ))

    # create regex for yellow positions
    for c in ye.keys():
        # the word must contain this char
        regex_list.append(re.compile(
            "^(.*[" + c + "].*)"
        ))

        # the word must not be in any previous positions
        for i in ye[c]:
            regex_list.append(re.compile(
                "^(?!.{" + str(i) + "}[" + c + "])"
            ))

    # second regex to exclude chars that aren't in the word
    regex_list.append(re.compile(
        "[^" + gy + "]{" + str(len(w)) + "}"
    ))

    new_words = prev_word_list
    for rule in regex_list:
        print(rule)
        new_words = list(filter(rule.match, new_words))

    return new_words, ye, gy, gn


with open("resources/wordle_allowed.txt", 'rt') as nw:
    all_words = np.array([line.rstrip() for line in nw])

words = all_words

print("first word recommendation: sores")

result = ""

while result != "GGGGG":

    input_word = input("Enter the word you input: ")
    result = input("Enter the result of inputting your first word (example: YGYXX) ")
    words, yellow, gray, green = generate_new_word_list(input_word, result, words, yellow, gray, green)

    # redeclare scores after each pass.
    scores = dict()

    for word in words:
        check = re.compile(generate_usability_regex(word))
        scores[word] = len(list(filter(check.match, words))) * len(list(filter(check.match, all_words)))

    print([(w, scores[w]) for w in words])

    print("next word recommendation:" + max(scores, key=scores.get))
