import nltk
import re

f = open('search_results.tx','r')
sentence = f.read()
tokens = nltk.word_tokenize(sentence)
for tok in tokens:
	if tok in ['.','@',',','..','...','&',';','-','!','?','+','_','__']:
		tokens.remove(tok)
print tokens

f.close()