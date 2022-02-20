import re
import sys
import numpy as np

scores = dict()

yellow = ""
gray = ""
green = []


def extend(list1, list2):
    for i in list2:
        list1.append(i)
    return list1

# all the words that are run on this function will already follow the gray/green/yellow rules.
# this regex will allow words which have any
def generate_usability_regex(w):
    output = ""
    for i in range(len(w)):
        output += "^.{" + str(i) + "}[" + w[i] + "]|"
    return output[:-1]


def generate_new_word_list(w, r, prev_word_list, ye, gy, gn):
    regex1 = "^"
    zipped = tuple(zip(range(len(w)), w, r))
    print("zipped", zipped)

    yel = ye + "".join(set([a for (i, a, b) in zipped if b == "Y" and a not in ye]))
    print("yel", yel)

    gre = extend(gn, [(i, a) for (i, a, b) in zipped if b == "G" and a not in [gw for (i, gw) in gn]])
    gry = gy + "".join(set([a for (i, a, b) in zipped if b == "X" and a not in gy]))

    # remove any greens from yellow and gray if they were added in this round
    for (i, a) in gre:
        yel = yel.replace(a, "")
        gry = gry.replace(a, "")

    cursor = 0

    # create regex for green positions
    for (i, a) in green:
        print("i", i, cursor)

        rel_position = i - cursor
        regex1 += "(.{" + str(rel_position) + "}[" + str(a) + "])"
        cursor = i + 1

    if len(yel) > 0:
        regex1 += "(.*[%a].*)" % yel

    # second regex to exclude chars that aren't in the word
    regex2 = "[^" + gry + "]{" + str(len(w)) + "}"

    listRE = re.compile(regex1)
    grayRE = re.compile(regex2)

    return list(filter(grayRE.match, filter(listRE.match, prev_word_list))), yel, gry, gre


with open("wordle_allowed.txt", 'rt') as nw:
    words = np.array([line.rstrip() for line in nw])

print("first word recommendation: sores")
for go in range(6):

    input_word = input("Enter the word you input ")
    result = input("Enter the result of inputting your first word (example: YGYXX) ")
    words, yellow, gray, green = generate_new_word_list(input_word, result, words, yellow, gray, green)

    scores = dict()

    for word in words:
        check = re.compile(generate_usability_regex(word))
        # this function takes too long! and it's rubbish anyway (too much use of repeating chars)
        scores[word] = len(list(filter(check.match, words)))

    print("word recommendation:" + max(scores, key=scores.get))
