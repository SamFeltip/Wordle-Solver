import random
import numpy as np
import wordle as wdl
import wordle.solver as ws


def return_score(guess, answer):
    repeat_count = {c: answer.count(c) for c in answer}
    output = ""

    for i in range(len(answer)):
        if guess[i] == answer[i]:
            output += 'G'
            repeat_count[answer[i]] -= 1
        elif guess[i] in answer and repeat_count[guess[i]] > 0:
            output += 'Y'
            repeat_count[guess[i]] -= 1
        else:
            output += 'X'

    return output


def play_wordle(answer):
    words = wdl.answer_words
    result = ""

    history = {"yellow": dict(), "grey": dict(), "green": dict()}

    # ideal best word has been precalculated, it takes a long time to run over every word in the dictionary, so
    # this speeds it up a bit

    turns = 0
    guess_word = "sores"
    while result != "GGGGG":
        print(guess_word, " (", answer, ")")
        result = return_score(guess_word, answer)
        guess_word, history = ws.play_round(guess_word, result, words, history)
        turns += 1

    return turns


def test(turns):
    total = 0
    for i in range(turns):
        answer = wdl.answer_words[random.randint(0, len(wdl.answer_words))]
        turns_taken = play_wordle(answer)
        print("answer: ", answer, ". turns taken: ", turns_taken)
        total += turns_taken

    return total / turns


average_time_taken = test(100)

print("average turns taken: ", average_time_taken)