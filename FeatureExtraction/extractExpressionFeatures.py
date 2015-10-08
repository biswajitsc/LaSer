# coding: utf-8
import re
import sys
import math
from convertMathMLExpression import *

def extract_MathMLUnigrams(mathML) :
	unigrams = set()
	
	for line in mathML :
		words = line.split(' ')
		for word in words :
			if (len(word) > 0) :
				unigrams.add(word)
	print "Unigrams of MathML equations Extracted"

	numDocs = len(mathML)
	idf_scores = {}

	unigrams_postinglist = {}
	for unigram in unigrams :
		unigrams_postinglist[unigram] = []
		idf_scores[unigram] = 0

	i = 0
	for line in mathML :
		i += 1
		for unigram in unigrams :
			string = str(unigram)
			if string in line :
				unigrams_postinglist[unigram].append((i, line.count(string)))
				idf_scores[unigram] += 1
	print "Unigram Features Postings List of MathML equations created"	
	return (unigrams, unigrams_postinglist, idf_scores)


def main() :
	input_file = open(sys.argv[1],"r")
	output_file_unigrams = open("../../Data/UnigramFeatures","w")
	output_file_bigrams = open("../../Data/BigramFeatures","w")
	output_file_trigrams = open("../../Data/TrigramFeatures","w")
	output_file_expressions = open("../../Data/ExtractedExpressions","w")
	output_file_idfs = open("../../Data/IDF-Scores","w")
	data = input_file.read()
	data = data.replace("\n"," ")
	lines = data.split('<m:math')
	mathML = []
	for line in lines :
		temp_line = line
		line = line.replace("<m:","<")
		line = line.replace("</m:","</")
		line = line.replace('\n', ' ')
		symbol = unicode(line, "utf-8")
		line = symbol.encode('ascii', 'backslashreplace')
		if len(line) == 0 :
			continue
		line = '<math' + line
		xmls = line.split('<?xml version="1.0"?>')
		for xml in xmls :
			xml = re.sub(' +',' ',xml)
			xml = xml.replace('\t', ' ')
			mathML.append(xml)

	(unigrams_mathML, unigrams_postinglist, idf_scores) = extract_MathMLUnigrams(mathML)
	expressions = convertEquation(mathML)

	for expression in expressions :
		output_file_expressions.write(expression.encode('utf-8') + '\n')

	unigrams = set()
	bigrams = set()
	trigrams = set()
	for line in expressions :
		line = line.encode('utf-8')
		words = line.split(' ')
		for word in words :
			if (len(word) > 0) :
				unigrams.add(word)
	print "Unigrams of expressions Extracted"
	
	for line in expressions :
		line = line.encode('utf-8')
		words = line.split(' ')
		if len(words) >= 2 :
			i = 0
			while (i < (len(words) - 1)) :
				if (len(words[i]) > 0 and len(words[i + 1]) > 0) :
					bigrams.add((words[i],words[i + 1]))
				i += 1
	print "Bigrams of expressions Extracted"
	for line in expressions :
		line = line.encode('utf-8')
		words = line.split(' ')
		if len(words) > 2 :
			i = 0
			while (i < (len(words) - 2)) :
				if (len(words[i]) > 0 and len(words[i + 1]) > 0 and len(words[i + 2]) > 0) :	
					trigrams.add((words[i],words[i + 1],words[i + 2]))
				i += 1
	print "Trigrams of expressions Extracted"
	
	print "Unigrams in MathML : ", len(unigrams_mathML), ", Unigrams in Expression : ", len(unigrams), ", Bigrams in Expression : ", len(bigrams), ", Trigrams in Expression : ", len(trigrams)

	numDocs = len(mathML)

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

	i = 0
	for line in expressions :
		line = line.encode('utf-8')
		i += 1
		for unigram in unigrams :
			string = str(unigram)
			if string in line :
				unigrams_postinglist[unigram].append((i, line.count(string)))
				idf_scores[unigram] += 1
	print "Unigram Features Postings List created"
	
	i = 0
	for line in expressions :
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
	for line in expressions :
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

	# i = 0
	# weight_matrix = []
	# for line in mathML :
	# 	values = {}
	# 	i += 1
	# 	if (i % 100 == 0) :
	# 		print str(i) + "th xml's weights written"
	# 	for unigram in unigrams :
	# 		for doc_id_weight_pair in unigrams_postinglist[unigram] :
	# 			if doc_id_weight_pair[0] == i :	
	# 				values[unigram] = (idf_scores[unigram] * (1 + math.log(doc_id_weight_pair[1])))
	# 			else :
	# 				values[unigram] = idf_scores[unigram]
	# 	for bigram in bigrams :
	# 		for doc_id_weight_pair in bigrams_postinglist[bigram] :
	# 			if doc_id_weight_pair[0] == i :	
	# 				values[bigram] = (idf_scores[bigram] * (1 + math.log(doc_id_weight_pair[1])))
	# 			else :
	# 				values[bigram] = idf_scores[bigram]
	# 	for trigram in trigrams :
	# 		for doc_id_weight_pair in trigrams_postinglist[trigram] :
	# 			if doc_id_weight_pair[0] == i :	
	# 				values[trigram] = (idf_scores[trigram] * (1 + math.log(doc_id_weight_pair[1])))
	# 			else :
	# 				values[trigram] = idf_scores[trigram]
	# 	weight_matrix.append(values)		
	# 	# output_file_weights.write(str(values) + '\n')
	# return weight_matrix

if __name__ == "__main__" :
	main()