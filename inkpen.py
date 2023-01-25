import math

sentense_sliptters = ['.', '?', '!', '…', ';', ':']
word_sliptters = ['-', ',', ' ', '"', '”', '“', '[', ']', '(', ')', '{', '}', '»', '«', 'ⓣ', '%', '*', '_', '/', '\\',
                  '№', '–']


def getSplit(text, splitters):
    text = text.lower()
    arr = []
    s = ''
    for c in text:
        if c in splitters:
            s = s.strip()
            if len(s) > 0:
                arr.append(s)
            s = ''
        else:
            s += c
    s = s.strip()
    if len(s) > 0:
        arr.append(s)
    return arr


k = 2
dictionary = {}
pairs = {}
find_token = '|'

def checkWord(word):
    ok = True
    for i in range(10):
        if str(i) in word:
            ok = False
    return ok
def analyze():
    with open('my_corpus.txt', 'r', encoding="UTF8") as file:
        text = file.read().strip().lower()
        text = text.replace('\n', '')
        sentences = getSplit(text, sentense_sliptters)
        for sentence in sentences:
            words = getSplit(sentence, word_sliptters)
            for i in range(len(words)):

                word = words[i]

                if not checkWord(word):
                    continue
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

                if not (word in pairs):
                    pairs[word] = {}
                for j in range(1, k + 1):
                    if j != 0 and 0 <= i + j < len(words) and checkWord(words[i + j]):
                        if words[i + j] in pairs[word]:
                            pairs[word][words[i + j]] += 1
                        else:
                            pairs[word][words[i + j]] = 1
def count(word):
    if word in dictionary:
        return dictionary[word]
    else:
        return 0
def countPairs(word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()
    if word1 in pairs:
        if word2 in pairs[word1]:
            return pairs[word1][word2]
    return 0

def predict(text, ns):
    words = getSplit(text.strip().lower(), word_sliptters)
    arr = []
    prob = 0
    if find_token in words:
        ans = ''
        ind = words.index(find_token)
        for word in ns:
            words[ind] = word
            pmi = 0

            for i in range(max(0, ind - k), ind):
                if countPairs(words[i], word) > 0:
                    pmi += countPairs(words[i], word) / (count(word) + count(words[i]))
            for i in range(ind + 1, min(ind + k + 1, len(words))):
                if countPairs(word, words[i]) > 0:
                    pmi += countPairs(word, words[i]) / (count(word) + count(words[i]))

            if pmi > prob:
                prob = pmi
                ans = word
            arr.append([pmi, ' ' . join(words)])
        if ans == '':
            return [text, arr]
        else:
            words[ind] = ans
            return [' '.join(words), arr]
    else:
        return [text, arr]

analyze()

sinset = ['uyga', 'hovlimga', 'uyimga', 'uyiga', 'joyga', 'xonaga', 'manzilga']

print()
res = predict("men | bordim", sinset)[1]
res.sort(reverse=True)
for v in res[:10]:
    print("%-20s %.16f" % (v[1], v[0]))
