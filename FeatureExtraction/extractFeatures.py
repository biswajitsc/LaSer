import re
import sys

def main() :
	input_file = open(sys.argv[1],"r")
	output_file_unigrams = open("../../Data/UnigramFeatures","w")
	output_file_bigrams = open("../../Data/BigramFeatures","w")
	output_file_trigrams = open("../../Data/TrigramFeatures","w")
	data = input_file.read()
	lines = data.split('<m:math xmlns:m="http://www.w3.org/1998/Math/MathML" display="block">')
	mathML = []
	for line in lines :
		line = line.replace('\n', ' ')
		xml = line.split('<?xml version="1.0"?> <math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/1998/Math/MathML         http://www.w3.org/Math/XMLSchema/mathml2/mathml2.xsd">')
		for xmls in xml :
			xmls = re.sub(' +',' ',xmls)
			xmls = xmls.replace('\t', ' ')
			# print xmls
			mathML.append(xmls)
	unigrams = set()
	bigrams = set()
	trigrams = set()
	for line in mathML :
		words = line.split(' ')
		# print line, len(words)
		for word in words :
			if (len(word) > 0) :
				unigrams.add(word)
	for line in mathML :
		words = line.split(' ')
		# print line, len(words)
		if len(words) >= 2 :
			i = 0
			while (i < (len(words) - 1)) :
				if (len(words[i]) > 0 and len(words[i + 1]) > 0) :
					bigrams.add((words[i],words[i + 1]))
				i += 1
	for line in mathML :
		words = line.split(' ')
		if len(words) > 2 :
			i = 0
			while (i < (len(words) - 2)) :
				# print words[i], words[i + 1], words[i + 2], len(trigrams)
				if (len(words[i]) > 0 and len(words[i + 1]) > 0 and len(words[i + 2]) > 0) :	
					trigrams.add((words[i],words[i + 1],words[i + 2]))
				i += 1

	for unigram in unigrams :
		output_file_unigrams.write(unigram + '\n')
	for bigram in bigrams :
		output_file_bigrams.write(str(bigram) + '\n')
	for trigram in trigrams :
		output_file_trigrams.write(str(trigram) + '\n')

if __name__ == "__main__" :
	main()