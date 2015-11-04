# coding: utf-8
import re
import sys
import math


removeRareFeatures = False


def main() :
	input_file = open(sys.argv[1],"r")
	output_file_unigrams = open("../../Data/UnigramContextFeatures","w")
	output_file_bigrams = open("../../Data/BigramContextFeatures","w")
	output_file_trigrams = open("../../Data/TrigramContextFeatures","w")
	output_file_idfs = open("../../Data/ContextIDF-Scores","w")
	data = input_file.read()
	lines = data.split('\n')
	contexts = []
	for line in lines :
		symbol = unicode(line, "utf-8")
		line = symbol.encode('ascii', 'backslashreplace')
		if len(line) == 0 :
			continue
		line = re.sub(' +',' ',line)
		line = line.replace('\t', ' ')
		words = line.split(' ')[1:]
		line = ''
		for i in range(len(words)):
			if i < len(words) - 1:
				line += words[i] + " "
			else:
				line += words[i]
		contexts.append(line)

	unigrams = set()
	bigrams = set()
	trigrams = set()
	for line in contexts:
		line = line.encode('utf-8')
		words = line.split(' ')
		for word in words :
			if (len(word) > 0) :
				unigrams.add(word)
	print "Unigrams of contexts Extracted"
	
	for line in contexts :
		line = line.encode('utf-8')
		words = line.split(' ')
		if len(words) >= 2 :
			i = 0
			while (i < (len(words) - 1)) :
				if (len(words[i]) > 0 and len(words[i + 1]) > 0) :
					bigrams.add((words[i],words[i + 1]))
				i += 1
	print "Bigrams of contexts Extracted"
	
	for line in contexts :
		line = line.encode('utf-8')
		words = line.split(' ')
		if len(words) > 2 :
			i = 0
			while (i < (len(words) - 2)) :
				if (len(words[i]) > 0 and len(words[i + 1]) > 0 and len(words[i + 2]) > 0) :	
					trigrams.add((words[i],words[i + 1],words[i + 2]))
				i += 1
	print "Trigrams of contexts Extracted"
	
	print "Unigrams in Context : ", len(unigrams), ", Bigrams in Context : ", len(bigrams), ", Trigrams in Context : ", len(trigrams)

	numDocs = len(contexts)

	idf_scores = {}
	unigrams_postinglist = {}
	for unigram in unigrams :
		unigrams_postinglist[unigram] = []
		idf_scores[unigram] = 0

	bigrams_postinglist = {}
	for bigram in bigrams :
		bigrams_postinglist[bigram] = []
		idf_scores[bigram] = 0

	trigrams_postinglist = {}
	for trigram in trigrams :
		trigrams_postinglist[trigram] = []
		idf_scores[trigram] = 0
	print "Initialized weight matrices"

	i = 0
	for line in contexts:
		line = line.encode('utf-8')
		i += 1
		if (i % 100 == 0) :
                        print str(i) + "th xml checked for unigrams"
		for unigram in unigrams :
			string = str(unigram)
			if string in line :
				unigrams_postinglist[unigram].append((i, line.count(string)))
				idf_scores[unigram] += 1
	print "Unigram Features Postings List created"
	
	i = 0
	for line in contexts:
		line = line.encode('utf-8')
		i += 1
		if (i % 100 == 0) :
			print str(i) + "th xml checked for bigrams"
		for bigram in bigrams :
			string = (str(bigram[0]) + ' ' + str(bigram[1]))
			if string in line :
				bigrams_postinglist[bigram].append((i, line.count(string)))
				idf_scores[bigram] += 1
	print "Bigram Features Postings List created"
	
	i = 0
	for line in contexts:
		line = line.encode('utf-8')
		i += 1
		if (i % 100 == 0) :
			print str(i) + "th xml checked for trigrams"
		for trigram in trigrams :
			string = (str(trigram[0]) + ' ' + str(trigram[1]) + ' ' + str(trigram[2]))
			if string in line :
				trigrams_postinglist[trigram].append((i, line.count(string)))
				idf_scores[trigram] += 1
	print "Trigram Features Postings List created"

	if removeRareFeatures == True:
		i = 0
		for unigram in unigrams_postinglist.keys() :
			if len(unigrams_postinglist[unigram]) <= 5 :
				unigrams_postinglist.pop(unigram, None)
				i += 1
		print i, " rare Unigram features removed"

		i = 0
		for bigram in bigrams_postinglist.keys() :
			if len(bigrams_postinglist[bigram]) <= 5 :
				bigrams_postinglist.pop(bigram, None)
				i += 1
		print i, " rare Bigram features removed"

		i = 0
		for trigram in trigrams_postinglist.keys() :
			if len(trigrams_postinglist[trigram]) <= 5 :
				trigrams_postinglist.pop(trigram, None)
				i += 1
		print i, " rare Trigram features removed"

	output_file_unigrams.write(str(unigrams_postinglist))
	output_file_bigrams.write(str(bigrams_postinglist))
	output_file_trigrams.write(str(trigrams_postinglist))

	for features in idf_scores :
		idf_scores[features] = (1 + math.log(numDocs/idf_scores[features])) #check error
	output_file_idfs.write(str(idf_scores))

if __name__ == "__main__" :
	main()
