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
triplets = {}
find_token = '|'
cnt_words = 0
def checkWord(word):
    ok = True
    if not(1 <= len(word) <= 100):
        ok = False
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
                if not (word in triplets):
                    triplets[word] = {}
                for j in range(1, skip_size + 1):
                    if 0 <= i + j < len(words) and checkWord(words[i + j]):
                        if not(words[i + j] in pairs[word]):
                            pairs[word][words[i + j]] = 1
                        else:
                            pairs[word][words[i + j]] += 1

                        if not(words[i + j] in triplets[word]):
                            triplets[word][words[i + j]] = {}
                        for k in range(1, skip_size + 1):
                            if 0 <= i + j + k < len(words) and checkWord(words[i + j + k]):
                                if words[i + j + k] in triplets[word][words[i + j]]:
                                    triplets[word][words[i + j]][words[i + j + k]] += 1
                                else:
                                    triplets[word][words[i + j]][words[i + j + k]] = 1


def countTriplets(word1, word2, word3):
    word1 = word1.lower()
    word2 = word2.lower()
    word3 = word3.lower()
    if word1 in triplets:
        if word2 in triplets[word1]:
            if word3 in triplets[word1][word2]:
                return triplets[word1][word2][word3]
    return 0
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
        prprev_word = words[ind - 2]
        for word in dictionary:
            words[ind] = word
            p1 = countTriplets(prprev_word, prev_word, word)
            p2 = countPairs(prprev_word, prev_word)
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

corr = 0
all = 0

vec = [
    ["davlat tili |", "davlat tili to‘g‘risida"],
    ["oʻzbek tili davlat |", "oʻzbek tili davlat tili"],
    ["yo‘l qoidalarini yaxshi |", "yo‘l qoidalarini yaxshi biladi"],
    ["barcha tumanlarda |", "barcha tumanlarda chiqindilarni"],
    ["qanday qilib |", "qanday qilib bu"],
    ["universitetda o‘qish uchun davlat test |", "universitetda o‘qish uchun davlat test markazi"],
    ["halol mehnat |", "halol mehnat ortidan"],
    ["bir paytda ikki |", "bir paytda ikki tomonlama"],
    ["katta sahnaga |", "katta sahnaga ega"],
    ["respublika shoshilinch tibbiy |", "respublika shoshilinch tibbiy yordam"],
    ["oziq ovqat |", "oziq ovqat mahsulotlari"],
    ["bo‘lim boshlig‘i |", "bo‘lim boshlig‘i lavozimiga"],
    ["markaziy tashkilotlarning rasmiy |", "markaziy tashkilotlarning rasmiy xabarda"]
]

for v in vec:
    res = predict(v[0])
    ans, arr = res[0], res[1]
    if ans == v[1]:
        corr += 1
    all += 1

print(corr / all)