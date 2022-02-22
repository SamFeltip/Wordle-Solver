import wordle as wdl
import random

max_turns = 6
answer = wdl.answer_words[random.randint(0, len(wdl.answer_words))]

history = {"yellow": dict(), "grey": dict(), "green": dict()}

# ideal best word has been precalculated, it takes a long time to run over every word in the dictionary, so
# this speeds it up a bit
complete = False
turns = 0

while turns < max_turns and not complete:
    guess_word = ""
    while (len(guess_word) < 5) or (guess_word not in wdl.all_words):
        guess_word = input("guess: ").lower()

        if guess_word not in wdl.all_words:
            print("invalid word.")

    result = wdl.return_score(guess_word, answer)
    if result == "GGGGG":
        complete = True
    else:
        print("result: ", result)
    turns += 1

if complete:
    print("you got the word in ", turns, " guesses. The answer was ", answer)
else:
    print("the answer was ", answer)