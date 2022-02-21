import numpy as np
import re

# this regex will allow strings with any characters in the same position as the input word to pass.
# it is used to try and "score" a word for it's
def generate_usability_regex(w):
    output = ""
    for i in range(len(w)):
        output += "^.{" + str(i) + "}[" + w[i] + "]|"
    return output[:-1]


with open("../wordle/resources/wordle_allowed.txt", 'rt') as nw:
    all_words = np.array([line.rstrip() for line in nw])

with open("../wordle/resources/wordle_answers.txt", 'rt') as nw:
    answer_words = np.array([line.rstrip() for line in nw])

all_words = np.append(all_words, answer_words)

print("wordle package: finding initial scores for all words")
all_scores = dict()
for word in answer_words:
    scoreRE = re.compile(generate_usability_regex(word))
    all_scores[word] = len(list(filter(scoreRE.match, all_words)))

#
# sores
# canny
# tacit
# batch
# catch
# catch