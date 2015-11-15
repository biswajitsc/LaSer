# coding: utf-8

from lxml import etree
from StringIO import *
from lxml import objectify
import xml.etree.ElementTree as ET
import sympy
import re
import decimal
import unicodedata as ucode
import sys
import math
import os
import ast

def generateMathML(latex_eqn) :
	cleanEqn = latex_eqn.strip('\n').strip()
	cleanEqn = re.sub('\\\\','\\\\\\\\',cleanEqn)
	cleanEqn = re.sub('\)','\\\\)',cleanEqn)
	cleanEqn = re.sub('\(','\\\\(',cleanEqn)
	# print cleanEqn
	oscommand = 'latexmlmath --pmml=- ' + cleanEqn + ' > temp.txt'
	# print oscommand
	os.system(oscommand)
	return open('temp.txt','r').read()

def parseMML(mmlinput):
	mmlinput= mmlinput.replace(' xmlns="', ' xmlnamespace="')
	parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
	tree   = etree.parse(StringIO(mmlinput), parser)
	objectify.deannotate(tree,cleanup_namespaces=True,xsi=True,xsi_nil=True)
	mmlinput=etree.tostring(tree.getroot())
	exppy="" #this is the python expression
	symvars=[]  #these are symbolic variables which can eventually take part in the expression
	events = ("start", "end")
	level = 0
	context = etree.iterparse(StringIO(mmlinput),events=events)
	for action, elem in context:
		if (action=='start') and (elem.tag=='mfrac'):
			level += 1
			mmlaux=etree.tostring(elem[0])
			(a,b)=parseMML(mmlaux)
			symvars.append(b)
			exppy+=a
			exppy+='/'
			mmlaux=etree.tostring(elem[1])
			(a,b)=parseMML(mmlaux)
			symvars.append(b)
			exppy+=a
		if (action=='end') and (elem.tag=='{http://www.w3.org/1998/Math/MathML}mfrac'):
			level -= 1
		if level:
			continue
		if (action=='start') and (elem.tag=='{http://www.w3.org/1998/Math/MathML}mrow'):
			exppy+='('
		if (action=='end') and (elem.tag=='{http://www.w3.org/1998/Math/MathML}mrow'):
			exppy+=')'
		if elem.text == None :
			continue
		if action=='start' and elem.tag=='{http://www.w3.org/1998/Math/MathML}mn': #this is a number
			exppy+=elem.text
		if action=='start' and elem.tag=='{http://www.w3.org/1998/Math/MathML}mi': #this is a variable
			exppy+=elem.text
			symvars.append(elem.text) #we'll return the variable, so sympy can sympify it afterwards
		if action=='start' and elem.tag=='{http://www.w3.org/1998/Math/MathML}mo': #this is a operation
			exppy+=elem.text
	return (exppy, symvars)

def simplifyMathML(mathml_eqn) :
	return mathml_eqn
	# if (str(mathml_eqn) == '<?xml version="1.0" encoding="UTF-8"?>' or len(mathml_eqn) == 0) :
	# 	return ""
	# mathml_eqn = mathml_eqn.replace('\n',' ')
	# temp_mathml_eqn = mathml_eqn
	# try :
	# 	mathml_eqn = mathml_eqn.replace("<m:mo><U+2062></m:mo>","")
	# 	(expr, symbvars) = parseMML(mathml_eqn)
	# 	simp_expr = sympy.simplify(expr)
	# 	c_mathml = sympy.printing.mathml(simp_expr)
	# 	from sympy.utilities.mathml import c2p
	# 	p_mathml = c2p(c_mathml)
	# 	p_mathml = str(p_mathml)
	# 	p_mathml = p_mathml.replace('\n',' ')
	# 	return p_mathml
	# except Exception :
	# 	return ""

def numberNormalize(mathml_eqn) :
	# line = '<mn>2.45</mn>   <m:mn>2.45646</m:mn> <mn>2</mn>   <mn>2.45</mn>'
	matches = re.findall(r'<mn>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?</mn>', mathml_eqn)
	already_matched = set()
	normalizedLines = []
	normalizedLines.append(mathml_eqn)
	for match in matches :
		if len(match) > 0 :
			if match[0] not in already_matched :
				already_matched.add(match[0])
				d = decimal.Decimal(match[0])
				exp = abs(d.as_tuple().exponent)
				i = 0
				orig_string = '<mn>' + str(match[0]) + '</mn>'
				while i < exp :
					strng = '<mn>' + str(round(d, i)) + '</mn>'
					temp_line = mathml_eqn.replace(orig_string, strng)
					normalizedLines.append(temp_line)
					i += 1
	matches = re.findall(r'<m:mn>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?</m:mn>', mathml_eqn)
	already_matched = set()
	for match in matches :
		if len(match) > 0 :
			if match[0] not in already_matched :
				already_matched.add(match[0])
				d = decimal.Decimal(match[0])
				exp = abs(d.as_tuple().exponent)
				i = 0
				orig_string = '<m:mn>' + str(match[0]) + '</m:mn>'
				while i < exp :
					strng = '<m:mn>' + str(round(d, i)) + '</m:mn>'
					temp_line = mathml_eqn.replace(orig_string, strng)
					normalizedLines.append(temp_line)
					i += 1
	return normalizedLines
	
def unicodeNormalize(mathml_eqn) :
	lines = mathml_eqn.split('\n')
	normalizedString = ""
	for line in lines:
		tokens = line.split(' ')
		for token in tokens:
			startTag = '<m:mi>';
			endTag = '</m:mi>'
			normalized = False
			for iter in range(2):
				if (token.startswith(startTag)):
					st = token.find(startTag) + len(startTag)
					en = token.find(endTag)
					symbol = unicode(token[st:en], "utf-8")
					symbol = ucode.normalize('NFKD', symbol)
					symbol = symbol.encode('ascii', 'backslashreplace')
					normalizedString += startTag + symbol + endTag
					normalized = True
					break
				startTag = '<mi>'
				endTag = '</mi>'
			if not normalized:
				normalizedString += token

			normalizedString += ' '
		normalizedString += '\n'

	return normalizedString

map = {}

def initMap():
	fileName = "../Normalization/operator_groups.txt"
	data = open(fileName,'r').read()
	tokens = data.split('\n')
	id = 1

	for token in tokens:
		# print token
		operators = token.split(' ')
		for c in operators:
			if len(c) > 0:
				map[c] = "OP" + str(id)
		id += 1

	# for key in map:
	#     print key, map[key]

def addGroups(data):
	normalized = ''
	lines = data.split('\n')
	changed = False

	for line in lines:
		tokens = line.split(' ')
		for token in tokens:
			s1 = '<m:mo>'
			e1 = '</m:mo>'
			s2 = '<mo>'
			e2 = '</mo>'
			found = False
			if token.startswith(s1):
				st = token.find(s1) + len(s1)
				en = token.find(e1)
				op = token[st:en]
				if (op in map):
					normalized += s1 + map[op] + e1
					found = True
					changed = True
			elif token.startswith('<mo>'):
				st = token.find(s2) + len(s2)
				en = token.find(e2)
				op = token[st:en]
				if (op in map):
					normalized += s2 + map[op] + e2
					found = True
					changed = True

			if not found:
				normalized += token

			normalized += ' '
			normalized = normalized[:-1]
		normalized += '\n'
	normalized = normalized[:-1]
	if changed:
		return normalized
	else:
		return data

def operatorNormalize(mathml_eqn):
	initMap()
	normalized = addGroups(mathml_eqn)
	if mathml_eqn != normalized:
		return [mathml_eqn, addGroups(mathml_eqn)]
	else:
		return [mathml_eqn]

variations = []

def reduceExpression(terminalXml):
	
	global variations

	terminalXmlText = terminalXml.text
	terminalXmlTag = terminalXml.tag

	if terminalXmlText != None:
		terminalXmlText = terminalXmlText.strip()
		if terminalXmlText != '':
			variations.append(terminalXmlText)

	if terminalXmlTag != None:
		terminalXmlTag = terminalXmlTag.strip()
		if terminalXmlTag != '' and terminalXmlTag != 'mo' and terminalXmlTag != 'mi' and terminalXmlTag != 'mn' and terminalXmlTag != 'mrow' and terminalXmlTag != 'math':
			variations.append(terminalXmlTag)

def genTreeStructureUtil(rawXml):

	global variations

	if (len(list(rawXml))) <= 0:
		reduceExpression(rawXml)

	terminalXmlTag = rawXml.tag

	if terminalXmlTag != None:
		terminalXmlTag = terminalXmlTag.strip()
		if terminalXmlTag != '' and terminalXmlTag != 'mo' and terminalXmlTag != 'mi' and terminalXmlTag != 'mn' and terminalXmlTag != 'mrow' and terminalXmlTag != 'math':
			variations.append(terminalXmlTag)
	
	for child in rawXml:	
		genTreeStructureUtil(child)


def convertEquation(mathml_eqn) :

	global variations
	rawEq = mathml_eqn.strip('\n').replace('m:','')
	# rawEq = rawEq.replace('xmlns', '')
	# rawEq = rawEq.replace(':m', '')
	# rawEq = rawEq.replace(':mml', '')
	# rawEq = rawEq.replace('="http://www.w3.org/1998/Math/MathML"','')
	# rawEq = rawEq.replace(':xsi="http://www.w3.org/2001/XMLSchema-instance"','')
	# rawEq = rawEq.replace('xsi:schemaLocation="http://www.w3.org/1998/Math/MathML http://www.w3.org/Math/XMLSchema/mathml2/mathml2.xsd"', '')
	# # print rawEq
	expression = ""
	try:
		variations = []
		# print rawEq
		genTreeStructureUtil(ET.fromstring(rawEq))
		# print variations
		for variation in variations:
			expression += variation + ' '
		return expression
	except Exception as e:
		print e, mathml_eqn
		return mathml_eqn

def extract_MathMLUnigrams(mathML, idf_scores) :
	unigrams = set()
	
	words = mathML.split(' ')
	for word in words :
		if (len(word) > 0) :
			if word != 'display="block">':
				unigrams.add(word)
	print "Unigrams of MathML equations Extracted"

	weight_score = {}

	for unigram in unigrams :
		if '<mi>' in unigram :
			if unigram in idf_scores.keys() :
				print "Present"
			else :
				print "Not Present"
		if unigram in idf_scores.keys():
			weight_score[unigram] = ((1 + math.log(mathML.count(unigram))) * idf_scores[unigram])
				
	return weight_score

def extractContextWeights(context, idf_scores, unigrams, bigrams, trigrams):
	context = context.replace('\n', ' ')
	context = re.sub(' +',' ',context)
	context = context.replace('\t', ' ')

	symbol = context.encode("utf-8")
	context = symbol.encode('ascii', 'backslashreplace')

	unigrams_query = set()
	bigrams_query = set()
	trigrams_query = set()

	weight_score = {}

	words = context.split(' ')
	for word in words :
		if (len(word) > 0) :
			unigrams_query.add(word)
	print "Unigrams_query of context Extracted"
	
	words = context.split(' ')
	if len(words) >= 2 :
		i = 0
		while (i < (len(words) - 1)) :
			if (len(words[i]) > 0 and len(words[i + 1]) > 0) :
				bigrams_query.add((words[i],words[i + 1]))
			i += 1
	print "Bigrams_query of context Extracted"
	
	words = context.split(' ')
	if len(words) > 2 :
		i = 0
		while (i < (len(words) - 2)) :
			if (len(words[i]) > 0 and len(words[i + 1]) > 0 and len(words[i + 2]) > 0) :	
				trigrams_query.add((words[i],words[i + 1],words[i + 2]))
			i += 1
	print "Trigrams_query of context Extracted"
	
	for unigram in unigrams_query :
		string = str(unigram)
		if string in context and unigram in idf_scores.keys():
			weight_score[unigram] = ((1 + math.log(context.count(string))) * idf_scores[unigram])

	for bigram in bigrams_query :
		string = (str(bigram[0]) + ' ' + str(bigram[1]))
		if string in context and bigram in idf_scores.keys():
			print string, "occured"
			weight_score[bigram] = ((1 + math.log(context.count(string))) * idf_scores[bigram])
	
	for trigram in trigrams_query :
		string = (str(trigram[0]) + ' ' + str(trigram[1]) + ' ' + str(trigram[2]))
		if string in context and trigram in idf_scores.keys():
			print string, "occured"
			weight_score[trigram] = ((1 + math.log(context.count(string))) * idf_scores[trigram])

	print "in extractContextWeights : weight_score is ",weight_score

	return weight_score

def extractWeights(mathml_eqn, idf_scores, unigrams, bigrams, trigrams) :
	mathml_eqn = mathml_eqn.replace('\n', ' ')
	mathml_eqn = mathml_eqn.replace('<?xml version="1.0"?>', '')
	mathml_eqn = re.sub(' +',' ',mathml_eqn)
	mathml_eqn = mathml_eqn.replace('\t', ' ')

	# print "in extractWeights : equation is ",mathml_eqn
	# print "in extractWeights : unigrams are ",unigrams
	# print "in extractWeights : idf_scores are ",idf_scores

	symbol = unicode(mathml_eqn, "utf-8")
	mathml_eqn = symbol.encode('ascii', 'backslashreplace')

	unigrams_query = set()
	bigrams_query = set()
	trigrams_query = set()

	weight_score = extract_MathMLUnigrams(mathml_eqn, idf_scores)
	expression = convertEquation(mathml_eqn)
	expression = expression.encode('utf-8')

	words = expression.split(' ')
	for word in words :
		if (len(word) > 0) :
			unigrams_query.add(word)
	print "Unigrams_query of expressions Extracted"
	
	words = expression.split(' ')
	if len(words) >= 2 :
		i = 0
		while (i < (len(words) - 1)) :
			if (len(words[i]) > 0 and len(words[i + 1]) > 0) :
				bigrams_query.add((words[i],words[i + 1]))
			i += 1
	print "Bigrams_query of expressions Extracted"
	
	words = expression.split(' ')
	if len(words) > 2 :
		i = 0
		while (i < (len(words) - 2)) :
			if (len(words[i]) > 0 and len(words[i + 1]) > 0 and len(words[i + 2]) > 0) :	
				trigrams_query.add((words[i],words[i + 1],words[i + 2]))
			i += 1
	print "Trigrams_query of expressions Extracted"
	
	print "Mathml extract weight : ", mathml_eqn

	print "Expression : ", expression

	for unigram in unigrams_query :
		string = str(unigram)
		if string in expression and unigram in idf_scores.keys():
			print string, "occured"
			weight_score[unigram] = ((1 + math.log(expression.count(string))) * idf_scores[unigram])

	for bigram in bigrams_query :
		string = (str(bigram[0]) + ' ' + str(bigram[1]))
		if string in expression and bigram in idf_scores.keys():
			print string, "occured"
			weight_score[bigram] = ((1 + math.log(expression.count(string))) * idf_scores[bigram])
	
	for trigram in trigrams_query :
		string = (str(trigram[0]) + ' ' + str(trigram[1]) + ' ' + str(trigram[2]))
		if string in expression and trigram in idf_scores.keys():
			print string, "occured"
			weight_score[trigram] = ((1 + math.log(expression.count(string))) * idf_scores[trigram])

	print "in extractWeights : weight_score is ",weight_score

	return weight_score

def normalizeQuery(mathml_eqn) :
	# simplifiedMathML = simplifyMathML(mathml_eqn)
	# if simplifiedMathML = "" :
	# 	simplifiedMathML = mathml_eqn

	print "#########"
	print "in function normalizeQuery"
	print "the argument mathml_eqn is ", mathml_eqn
	print "#########"

	# mathml_eqn = unicodeNormalize(mathml_eqn)
	mathml_eqns = operatorNormalize(mathml_eqn)
	normalized_eqns = []
	for eqn in mathml_eqns :
		curr_normalized_eqns = numberNormalize(eqn)
		normalized_eqns += curr_normalized_eqns
	print "normalized_eqns are ", mathml_eqn
	print "#########"
	return normalized_eqns

def generateIndex(NormalizedMathML):
	print "generateIndex invoked"
	input_file_unigrams_postinglist = open("../../Data/UnigramFeatures","r").read().decode('cp1252', errors='ignore')
	input_file_bigrams_postinglist = open("../../Data/BigramFeatures","r").read().decode('cp1252', errors='ignore')
	input_file_trigrams_postinglist = open("../../Data/TrigramFeatures","r").read().decode('cp1252', errors='ignore')
	input_file_idf_scores = open("../../Data/IDF-Scores","r").read().decode('cp1252', errors='ignore')

	unigrams_postinglist = ast.literal_eval(input_file_unigrams_postinglist)
	bigrams_postinglist = ast.literal_eval(input_file_bigrams_postinglist)
	trigrams_postinglist = ast.literal_eval(input_file_trigrams_postinglist)
	idf_scores = ast.literal_eval(input_file_idf_scores)

	input_file_context_unigrams_postinglist = open("../../Data/UnigramContextFeatures","r").read().decode('cp1252', errors='ignore')
	input_file_context_bigrams_postinglist = open("../../Data/BigramContextFeatures","r").read().decode('cp1252', errors='ignore')
	input_file_context_trigrams_postinglist = open("../../Data/TrigramContextFeatures","r").read().decode('cp1252', errors='ignore')
	input_file_context_idf_scores = open("../../Data/ContextIDF-Scores","r").read().decode('cp1252', errors='ignore')

	context_unigrams_postinglist = eval(input_file_context_unigrams_postinglist)
	context_bigrams_postinglist = eval(input_file_context_bigrams_postinglist)
	context_trigrams_postinglist = eval(input_file_context_trigrams_postinglist)
	context_idf_scores = eval(input_file_context_idf_scores)
	
	unigrams = set()
	bigrams = set()
	trigrams = set()

	for x in unigrams_postinglist:
		unigrams.add(x)

	for x in bigrams_postinglist:
		bigrams.add(x)

	for x in trigrams_postinglist:
		trigrams.add(x)

	context_unigrams = set()
	context_bigrams = set()
	context_trigrams = set()

	for x in context_unigrams_postinglist:
		context_unigrams.add(x)

	for x in context_bigrams_postinglist:
		context_bigrams.add(x)

	for x in context_trigrams_postinglist:
		context_trigrams.add(x)

	input_file = open(NormalizedMathML,"r")
	data = input_file.read()
	lines = data.split('\n')
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
		# line = '<math' + line
		xmls = line.split('<?xml version="1.0"?>')
		for xml in xmls :
			xml = re.sub(' +',' ',xml)
			xml = xml.replace('\t', ' ')
			mathML.append(xml)

	# Weight matrix computation

	# i = 0
	# weight_matrix = []
	# for line in mathML :
	# 	values = {}
	# 	i += 1
	# 	if (i % 100 == 0) :
	# 		print str(i) + "th xml's weights written"
	# 	if (i % 100 == 0) :
	# 		break
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

	metadata = open("../../Data/NormalizedMathMLMeta.xml","r").readlines()
	original_metadata = open("../../Data/MathMLMeta.xml","r").readlines()
	original_eqns = open("../../Data/MathML.xml","r").readlines()
	context_lines = open("../../Data/equation_context.txt","r").readlines()

	return (unigrams, bigrams, trigrams, idf_scores, unigrams_postinglist, bigrams_postinglist, trigrams_postinglist, metadata, original_eqns, original_metadata, context_unigrams, context_bigrams, context_trigrams, context_idf_scores, context_unigrams_postinglist, context_bigrams_postinglist, context_trigrams_postinglist, context_lines)

(unigrams, bigrams, trigrams, idf_scores, unigrams_postinglist, bigrams_postinglist, trigrams_postinglist, metadata, original_eqns, original_metadata, context_unigrams, context_bigrams, context_trigrams, context_idf_scores, context_unigrams_postinglist, context_bigrams_postinglist, context_trigrams_postinglist, context_lines) = generateIndex("../../Data/NormalizedMathML.xml")