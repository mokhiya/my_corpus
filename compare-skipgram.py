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


skip_size = 2
dictionary = {}
pairs = {}
find_token = '|'

def checkWord(word):
    ok = True
    if not (1 <= len(word) <= 100):
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

                if not checkWord(word):
                    continue
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

                if not (word in pairs):
                    pairs[word] = {}
                for j in range(-skip_size, skip_size + 1):
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
    prob = 0
    if find_token in words:
        ans = ''
        ind = words.index(find_token)
        prev_word = words[ind - 1]
        for word in dictionary:
            words[ind] = word
            tmp = countPairs(prev_word, word) / (dictionary[prev_word] + dictionary[word])

            if tmp > prob:
                prob = tmp
                ans = word
            arr.append([tmp, ' ' . join(words)])
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
