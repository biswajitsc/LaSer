import sys
import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

def filterText(inp):
	clean_inp = ""
	inp_words = inp.split()
	for word in inp_words:
		if word not in stop and len(word) >= 3:
			clean_inp += word + ' '
	clean_inp = re.sub('\W+',' ',clean_inp)
	clean_inp = clean_inp.strip()
	return clean_inp
