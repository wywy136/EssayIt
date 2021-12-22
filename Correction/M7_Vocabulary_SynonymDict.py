import nltk
def lemmas(word):
    lemma1=[]
    lemma2=[]
    with open('../Correction/level-dic/dict_v_adj_adv/'+word+".txt","r") as f:
        count=0
        for line in f:
            if count%2==0:
                lemma1.append(line.strip("\n"))
            if count%2==1:
                lemma2.append(line_to_list(line.strip("\n")))
            count=count+1
    lemma_dict=dict(zip(lemma1,lemma2))
    return lemma_dict

def line_to_list(line):
    word_list=nltk.word_tokenize(line)
    return word_list

        