# 文件1：M7_Vocabulary_Open#打开文件，文本预处理，分句分词
# 函数名：Open
# 输入：无参数（函数中打开成段的.txt作文文本文件）
# 返回：分好句段的二维列表


def Open(art):
 # w=open(r"article.txt",'r')
 # article=w.read()
 article = art
 cutLineFlag = ["?", "!", "."]
 cutWordFlag = [" ", ",", ":"]
 sentences = []
 oneSentence = ""
 for word in article:
  if word not in cutLineFlag:
   oneSentence = oneSentence + word
  else:
   sentences.append(oneSentence)
   oneSentence = ""
 for i in range(len(sentences)):
  sentences[i] = sentences[i].lstrip()
  sentences[i] = sentences[i] + str(" ")

 wordlist = [[] for i in range(len(sentences))]
 word_seped = [[] for i in range(len(sentences))]
 for i in range(len(sentences)):
  oneword = ""
  for single in sentences[i]:
   if single not in cutWordFlag:
    oneword = oneword + single
   else:
    wordlist[i].append(oneword)
    oneword = ""

 for i in range(len(wordlist)):
  for j in range(len(wordlist[i])):
   word_seped[i] = [k for k in wordlist[i] if k != '']


 return word_seped
