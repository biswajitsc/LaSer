import re
import sys
import math

def main() :
	input_file = open(sys.argv[1],"r")
	output_file_unigrams = open("../../Data/UnigramFeatures","w")
	output_file_bigrams = open("../../Data/BigramFeatures","w")
	output_file_trigrams = open("../../Data/TrigramFeatures","w")
	output_file_idfs = open("../../Data/IDF-Scores","w")
	output_file_weights = open("../../Data/Weight-Scores","w")
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
	
	numDocs = len(mathML)
	feature_numDocs = {}

	unigrams_postinglist = {}
	for unigram in unigrams :
		unigrams_postinglist[unigram] = []
		feature_numDocs[unigram] = 0

	bigrams_postinglist = {}
	for bigram in bigrams :
		bigrams_postinglist[bigram] = []
		feature_numDocs[bigram] = 0

	trigrams_postinglist = {}
	for trigram in trigrams :
		trigrams_postinglist[trigram] = []
		feature_numDocs[trigram] = 0

	i = 0
	for line in mathML :
		i += 1
		for unigram in unigrams :
			string = str(unigram)
			if string in line :
				unigrams_postinglist[unigram].append((i, line.count(string)))
				feature_numDocs[unigram] += 1
	print "Unigram Features Postings List created"
	
	i = 0
	for line in mathML :
		i += 1
		if (i % 100 == 0) :
			print str(i) + "th xml checked for bigrams"
		for bigram in bigrams :
			string = (str(bigram[0]) + ' ' + str(bigram[1]))
			if string in line :
				bigrams_postinglist[bigram].append((i, line.count(string)))
				feature_numDocs[bigram] += 1
	print "Bigram Features Postings List created"
	
	i = 0
	for line in mathML :
		i += 1
		if (i % 100 == 0) :
			print str(i) + "th xml checked for trigrams"
		for trigram in trigrams :
			string = (str(trigram[0]) + ' ' + str(trigram[1]) + ' ' + str(trigram[2]))
			if string in line :
				trigrams_postinglist[trigram].append((i, line.count(string)))
				feature_numDocs[trigram] += 1
	print "Trigram Features Postings List created"

	for unigram in unigrams :
		output_file_unigrams.write("{" + str(unigram) + " : " + str(unigrams_postinglist[unigram]) + "}" + '\n')
	for bigram in bigrams :
		output_file_bigrams.write("{" + str(bigram) + " : " + str(bigrams_postinglist[bigram]) + "}" + '\n')
	for trigram in trigrams :
		output_file_trigrams.write("{" + str(trigram) + " : " + str(trigrams_postinglist[trigram]) + "}" + '\n')
	for features in feature_numDocs :
		output_file_idfs.write(str(features) + " : " + str(1 + math.log(numDocs/feature_numDocs[features])) + '\n')
		feature_numDocs[features] = (1 + math.log(numDocs/feature_numDocs[features]))

	i = 0
	weight_matrix = []
	for line in mathML :
		values = {}
		i += 1
		if (i % 100 == 0) :
			print str(i) + "th xml's weights written"
		for unigram in unigrams :
			if unigrams_postinglist[unigram][0] == i :
				values[unigram] = (feature_numDocs[unigram] * (1 + math.log(unigrams_postinglist[unigram][1])))
			else :
				values[unigram] = feature_numDocs[unigram]
		for bigram in bigrams :
			if bigrams_postinglist[bigram][0] == i :
				values[bigram] = (feature_numDocs[bigram] * (1 + math.log(bigrams_postinglist[bigram][1])))
			else :
				values[bigram] = feature_numDocs[bigram]
		for trigram in trigrams :
			if trigrams_postinglist[trigram][0] == i :
				values[trigram] = (feature_numDocs[trigram] * (1 + math.log(trigrams_postinglist[trigram][1])))
			else :
				values[trigram] = feature_numDocs[trigram]
		weight_matrix.append(values)		
		output_file_weights.write(str(values) + '\n')

	return weight_matrix						

if __name__ == "__main__" :
	main()