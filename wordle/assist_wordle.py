import wordle as wdl

words = wdl.answer_words
result = ""

history = {"yellow": dict(), "grey": dict(), "green": dict(), "regex": set()}

turns = 0
guess_word = "crane"
print("first word: crane")
while result != "GGGGG":
    guess_word = input("guess: ")
    result = input("result: ")
    guess_word, history = wdl.play_round(guess_word, result, words, history)
    print("next word: ", guess_word)

print("word found!")