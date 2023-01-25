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


skip_size = 1
dictionary = {}
pairs = {}
find_token = '|'
cnt_words = 0

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
                global cnt_words
                cnt_words += 1
                if not checkWord(word):
                    continue
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

                if not (word in pairs):
                    pairs[word] = {}
                for j in range(1, skip_size + 1):
                    if j != 0 and 0 <= i + j < len(words) and checkWord(words[i + j]):
                        if words[i + j] in pairs[word]:
                            pairs[word][words[i + j]] += 1
                        else:
                            pairs[word][words[i + j]] = 1


def countPairs(word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()
    if word1 in pairs:
        if word2 in pairs[word1]:
            return pairs[word1][word2]
    return 0


def predict(text):
    words = getSplit(text.strip().lower(), word_sliptters)
    arr = []
    if find_token in words:
        prob = 0
        ans = ''
        ind = words.index(find_token)
        prev_word = words[ind - 1]
        for word in dictionary:
            words[ind] = word
            p1 = countPairs(prev_word, word)
            p2 = dictionary[prev_word]
            if p1 > 0:
                if p1 / p2 > prob:
                    prob = p1 / p2
                    ans = word
                arr.append([p1 / p2, ' ' . join(words)])
        if ans == '':
            return [text, arr]
        else:
            words[ind] = ans
            return [' '.join(words), arr]
    else:
        return [text, arr]

analyze()
res = predict("davlat tili |")[1]
res.sort(reverse=True)
for v in res[:20]:
    print("%-30s %.16f" % (v[1], v[0]))



