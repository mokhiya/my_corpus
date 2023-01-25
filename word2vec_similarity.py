from gensim.models import Word2Vec

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
with open('my_corpus.txt', encoding="UTF8") as file:
    text = file.read().strip().lower()
    text = text.replace('\n', '')
    arr = []
    sentences = getSplit(text, sentense_sliptters)
    for sentence in sentences:
        words = getSplit(sentence, word_sliptters)
        if len(words) > 0:
            arr.append(words)
    w1s0 = Word2Vec(sentences=arr, min_count=1, window=1, sg=0)
    w1s1 = Word2Vec(sentences=arr, min_count=1, window=1, sg=1)
    w5s0 = Word2Vec(sentences=arr, min_count=1, window=5, sg=0)
    w5s1 = Word2Vec(sentences=arr, min_count=1, window=5, sg=1)

    print("method=cbow, window=1")
    for v in w1s0.wv.most_similar('mehnat'):
        print("%-20s %.10f" % v)

    print("method=skipgram, window=1")
    for v in w1s1.wv.most_similar('mehnat'):
        print("%-20s %.10f" % v)

    print("method=cbow, window=5")
    for v in w5s0.wv.most_similar('mehnat'):
        print("%-20s %.10f" % v)

    print("method=skipgram, window=5")
    for v in w5s1.wv.most_similar('mehnat'):
        print("%-20s %.10f" % v)
