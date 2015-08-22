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
	print "Unigrams Extracted"
	for line in mathML :
		words = line.split(' ')
		# print line, len(words)
		if len(words) >= 2 :
			i = 0
			while (i < (len(words) - 1)) :
				if (len(words[i]) > 0 and len(words[i + 1]) > 0) :
					bigrams.add((words[i],words[i + 1]))
				i += 1
	print "Bigrams Extracted"
	for line in mathML :
		words = line.split(' ')
		if len(words) > 2 :
			i = 0
			while (i < (len(words) - 2)) :
				# print words[i], words[i + 1], words[i + 2], len(trigrams)
				if (len(words[i]) > 0 and len(words[i + 1]) > 0 and len(words[i + 2]) > 0) :	
					trigrams.add((words[i],words[i + 1],words[i + 2]))
				i += 1
	print "Trigrams Extracted"
	unigrams_postinglist = {}
	for unigram in unigrams :
		unigrams_postinglist[unigram] = []
	i = 0
	for line in mathML :
		i += 1
		for unigram in unigrams :
			if unigram in line :
				unigrams_postinglist[unigram].append(i)
	print "Unigram Features Postings List created"
	bigrams_postinglist = {}
	for bigram in bigrams :
		bigrams_postinglist[bigram] = []
	i = 0
	for line in mathML :
		i += 1
		if (i % 100 == 0) :
			print str(i) + "th xml checked for bigrams"
		for bigram in bigrams :
			if (str(bigram[0]) + ' ' + str(bigram[1])) in line :
				bigrams_postinglist[bigram].append(i)
	print "Bigram Features Postings List created"
	trigrams_postinglist = {}
	for trigram in trigrams :
		trigrams_postinglist[trigram] = []
	i = 0
	for line in mathML :
		i += 1
		if (i % 100 == 0) :
			print str(i) + "th xml checked for trigrams"
		for trigram in trigrams :
			if (str(trigram[0]) + ' ' + str(trigram[1]) + ' ' + str(trigram[2])) in line :
				trigrams_postinglist[trigram].append(i)
	print "Trigram Features Postings List created"	
	for unigram in unigrams :
		output_file_unigrams.write("{" + str(unigram) + " : " + str(unigrams_postinglist[unigram]) + "}" + '\n')
	for bigram in bigrams :
		output_file_bigrams.write("{" + str(bigram) + " : " + str(bigrams_postinglist[bigram]) + "}" + '\n')
	for trigram in trigrams :
		output_file_trigrams.write("{" + str(trigram) + " : " + str(trigrams_postinglist[trigram]) + "}" + '\n')

if __name__ == "__main__" :
	main()