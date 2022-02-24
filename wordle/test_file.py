import regex as re


def check_ap(word):
    rules = list()
    rules.append(re.compile('^(?!.{4}[e])'))
    rules.append(re.compile('[^t]{5}'))
    rules.append(re.compile('[^n]{5}'))
    rules.append(re.compile('[^d]{5}'))
    rules.append(re.compile('^(?!.{1}[b])'))
    rules.append(re.compile('^(?!.{4}[d])'))
    rules.append(re.compile('^(?!.{2}[t])'))
    rules.append(re.compile('^(?!.{0}[f])'))
    rules.append(re.compile('^(?!.{2}[a])'))
    rules.append(re.compile('^(.{3}[e])'))
    rules.append(re.compile('^(.*[a].*)'))
    rules.append(re.compile('^(?!.{3}[a])'))
    rules.append(re.compile('^(.*[l].*)'))
    rules.append(re.compile('^(?!.{1}[r])'))
    rules.append(re.compile('^(?!.{1}[e])'))
    rules.append(re.compile('^(?!.{4}[l])'))
    rules.append(re.compile('^(?!.{0}[c])'))
    rules.append(re.compile('^(.{0}[a])'))
    rules.append(re.compile('^(?!.{2}[l])'))
    rules.append(re.compile('[^c]{5}'))
    rules.append(re.compile('^(?!.{3}[n])'))
    rules.append(re.compile('^(.*[e].*)'))
    rules.append(re.compile('[^b]{5}'))
    rules.append(re.compile('[^r]{5}'))

    for rule in rules:
        print(rule)
        if not bool(re.match(rule, word)):
            return False
    return True


print(check_ap('alley'))
