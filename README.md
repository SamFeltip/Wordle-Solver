# Description
This is a basic python wordle solving program.

# How to use

## Parameters
This program has no parameters. Just run wordle/assist_wordle.py as a python script.

## Libraries
- re
- sys
- numpy

## User interface
You'll receive a recommended word on boot, and you'll then need to input the word you put into the game, followed by the score you received back.
Scores are encoded as 5 character strings, where:

- Gray squares are represented as "X"
- Yellow squares are represented as "Y"
- Green squares are represented as "G"

![example of a wordle score: each character in the word WATCH is highlighted as Gray, Green, Yellow, Yellow, Gray](resources/wordle_example.png)

This wordle score would be encoded as "XGYYX"

# Code quality
This code is quite messy and there are a number of improvements that can be made.

## Grading words
Words are currently graded based on the number of words in the collection of valid words (given gray, green & yellow rules) which share a given character in a given position.

If our library was `[stray, wants,stage,sheep,nouns,plain]` the word `stray` would receive a grade of 3, because `stage` and `sheep` both have "s" as their first character (it also shares characters with itself, trivially).

This obviously has issues. The grade does not consider characters that could be present in the word but in a different location. 
An ideal score would find the best word for ruling out as many words in the valid word collection as possible.

## Error catching
If you mistype your input word or score, the program will run as normal and potentially crash.

## Termination
The program will terminate when a wordle score of "GGGGG" is given.

# Performance
This program is rubbish, and I haven't bothered to test its average word location time.

# Wordle
If you've been living under a rock, and you don't know what wordle is, it's available [here (nytimes.com)](https://www.nytimes.com/games/wordle/index.html).
