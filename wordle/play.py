import wordle as wdl
import wordle.solver as ws

words = wdl.answer_words
result = ""

history = {"yellow": dict(), "grey": dict(), "green": dict()}

turns = 0
guess_word = "sores"
while result != "GGGGG":
    guess_word = input("guess: ")
    result = input("result: ")
    guess_word, history = ws.play_round(guess_word, result, words, history)
    print("next word: ", guess_word)
