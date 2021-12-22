import nltk
from nltk.stem import WordNetLemmatizer
def isverb(pos):
    if pos == 'VB' or pos == 'VBG' or pos == 'VBP' or pos == 'VBN' or pos == 'VBD' or pos == 'JJ' or pos == 'JJR' or pos == 'JJS' or pos == 'RB' or pos == 'RBR' or pos == 'RBS':
        return True
    else:
        return False

def lemmatize(tags):
    wnl = WordNetLemmatizer()
    pos = 'others'
    if tags[1] == 'VB' or tags[1] == 'VBP' or tags[1] == 'VBN' or tags[1] == 'VBG' or tags[1] == 'VBZ':
        pos = 'verb'
        return wnl.lemmatize(tags[0], pos='v').lower(), pos
    elif tags[1] == 'JJ' or tags[1] == 'JJR' or tags[1] == 'JJS':
        pos = 'adj.'
        return wnl.lemmatize(tags[0], pos='a').lower(), pos
    elif tags[1] == 'RB' or tags[1] == 'RBR' or tags[1] == 'RBS':
        pos = 'adv.'
        return wnl.lemmatize(tags[0], pos='r').lower(), pos
    else:
        return tags[0].lower(), pos


def Processdict(word_seped):
    processed = []
    processed_raw = []
    tags=[]

    for sent in word_seped:
        tags.append(nltk.pos_tag(sent))

    for i in range(len(tags)):
        ha = []
        processed.append(ha)
        for p in tags[i]:
            processed[i].append(lemmatize(p))

    for i in range(len(tags)):
        ha = []
        processed_raw.append(ha)
        for p in tags[i]:
            processed_raw[i].append(lemmatize(p)[0])
    return processed, processed_raw










