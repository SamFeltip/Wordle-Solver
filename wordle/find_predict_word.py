import wordle as wdl
import regex

def find_mediator_words(possible_answers, greens, answer_list):
    chars = list()

    for word in possible_answers:
        chars.extend(word)

    char_count = {a: chars.count(a) for a in chars if a not in greens}
    ordered_chars = sorted(char_count.keys(), key=lambda d: -char_count[d])

    reg = ""
    for c in ordered_chars:
        reg += "(?=\w*" +c+ ")"

    mediator_words = list()
    index = 1

    # while no mediator words have been found...
    while len(mediator_words) == 0:
        # begin by trying to find a word containing every character in every available word.
        # if a word cannot be found, remove the least common letter, and repeat until a word is found.

        reg += "\w+"
        r = regex.compile(reg)

        mediator_words = list(filter(r.match, answer_list))
        reg = reg[:-11]

    return mediator_words

# examples of possible inputs:
# find_mediator_words(['drone', 'drove', 'erode', 'froze', 'grope', 'grove', 'prone', 'prove', 'trope', 'trove', 'wrote'], ['o', 'e', 'r'], wdl.answer_words)

# XGGXG

# predict(['drone', 'drove', 'erode', 'froze', 'grope', 'grove', 'prone', 'prove', 'trope', 'trove', 'wrote'], ['o', 'e', 'r'], wdl.answer_words)

# dn dv ed fz gp gv pn pv tp tv wt

# d: 3
# n:
#
