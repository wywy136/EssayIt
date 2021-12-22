def is_not_all_punct(word):
 word=list(word)
 for letter in word:
  if letter.isalpha()==True or letter.isdigit()==True:
   return True
 return False

def Division(sentences):
 cutWordFlag = [" ", " , ", ":",'"']
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
   word_seped[i] = [k for k in wordlist[i]]

 for i in range(len(word_seped)):
   for j in range(len(word_seped[i])):
     for k in word_seped[i]:
       if is_not_all_punct(k)==False:
          word_seped[i].remove(k)

 return word_seped