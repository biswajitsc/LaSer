# coding: utf-8

from lxml import etree
from StringIO import *
from lxml import objectify
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
	if (str(mathml_eqn) == '<?xml version="1.0" encoding="UTF-8"?>' or len(mathml_eqn) == 0) :
		return ""
	mathml_eqn = mathml_eqn.replace('\n',' ')
	temp_mathml_eqn = mathml_eqn
	try :
		mathml_eqn = mathml_eqn.replace("<m:mo><U+2062></m:mo>","")
		(expr, symbvars) = parseMML(mathml_eqn)
		simp_expr = sympy.simplify(expr)
		c_mathml = sympy.printing.mathml(simp_expr)
		from sympy.utilities.mathml import c2p
		p_mathml = c2p(c_mathml)
		p_mathml = str(p_mathml)
		p_mathml = p_mathml.replace('\n',' ')
		return p_mathml
	except Exception :
		return ""

def numberNormalize(mathml_eqn) :
	# line = '<mn>2.45</mn>   <m:mn>2.45646</m:mn> <mn>2</mn>   <mn>2.45</mn>'
	matches = re.findall(r'<mn>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?</mn>', mathml_eqn)
	already_matched = set()
	for match in matches :
		if len(match) > 0 :
			if match[0] not in already_matched :
				already_matched.add(match[0])
				d = decimal.Decimal(match[0])
				exp = abs(d.as_tuple().exponent)
				strng = '<mn>' + str(match[0]) + '</mn>'
				i = 0
				while i < exp :
					strng += '<mn>' + str(round(d, i)) + '</mn>'
					i += 1
				orig_string = '<mn>' + str(match[0]) + '</mn>'
				mathml_eqn = mathml_eqn.replace(orig_string, strng)
	matches = re.findall(r'<m:mn>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?</m:mn>', mathml_eqn)
	already_matched = set()
	for match in matches :
		if len(match) > 0 :
			if match[0] not in already_matched :
				already_matched.add(match[0])
				d = decimal.Decimal(match[0])
				exp = abs(d.as_tuple().exponent)
				strng = '<m:mn>' + str(match[0]) + '</m:mn>'
				i = 0
				while i < exp :
					strng += '<m:mn>' + str(round(d, i)) + '</m:mn>'
					i += 1
				orig_string = '<m:mn>' + str(match[0]) + '</m:mn>'
				mathml_eqn = mathml_eqn.replace(orig_string, strng)
	return mathml_eqn
	
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
            map[c] = "OP" + str(id)
        id += 1

    # for key in map:
    #     print key, map[key]

def addGroups(data):
    normalized = ''
    lines = data.split('\n')

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
            elif token.startswith('<mo>'):
                st = token.find(s2) + len(s2)
                en = token.find(e2)
                op = token[st:en]
                if (op in map):
                    normalized += s2 + map[op] + e2
                    found = True

            if not found:
                normalized += token

            normalized += ' '
        normalized += '\n'
    return normalized

def operatorNormalize(mathml_eqn):
    initMap()
    return [mathml_eqn, addGroups(mathml_eqn)]

def convertEquation(mathml_eqn) :
	try :
		string = mathml_eqn.replace(' xmlns="', ' xmlnamespace="')
		parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
		tree   = etree.parse(StringIO(string), parser)
		root = tree.getroot()
		tags = root.findall('.//')
		expression = ""
		for tag in tags :
			if tag.text == None or len(tag.text) == 0 :
				continue
			text = tag.text.strip()
			if len(text) != 0 :
				expression += text + " "
		return expression
	except Exception :
		print "Error parsing", mathml_eqn
		return mathml_eqn

def extractWeights(mathml_eqn, idf_scores, unigrams, bigrams, trigrams) :
	mathml_eqn = mathml_eqn.replace('\n', ' ')
	mathml_eqn = mathml_eqn.replace('<?xml version="1.0"?>', '')
	mathml_eqn = re.sub(' +',' ',mathml_eqn)
	mathml_eqn = mathml_eqn.replace('\t', ' ')

	# print "in extractWeights : equation is ",mathml_eqn
	# print "in extractWeights : unigrams are ",unigrams
	# print "in extractWeights : idf_scores are ",idf_scores


	weight_score = {}
	
	for unigram in unigrams :
		string = str(unigram)
		if string in mathml_eqn :
			weight_score[unigram] = ((1 + math.log(mathml_eqn.count(string))) * idf_scores[unigram])

	expression = convertEquation(mathml_eqn)

	for unigram in unigrams :
		string = str(unigram)
		if string in expression :
			weight_score[unigram] = ((1 + math.log(mathml_eqn.count(string))) * idf_scores[unigram])

	for bigram in bigrams :
		string = (str(bigram[0]) + ' ' + str(bigram[1]))
		if string in expression :
			weight_score[bigram] = ((1 + math.log(mathml_eqn.count(string))) * idf_scores[bigram])
	
	for trigram in trigrams :
		string = (str(trigram[0]) + ' ' + str(trigram[1]) + ' ' + str(trigram[2]))
		if string in expression :
			weight_score[trigram] = ((1 + math.log(mathml_eqn.count(string))) * idf_scores[trigram])

	# print "in extractWeights : weight_score is ",weight_score

	return weight_score

def normalizeQuery(mathml_eqn) :
	# simplifiedMathML = simplifyMathML(mathml_eqn)
	# if simplifiedMathML = "" :
	# 	simplifiedMathML = mathml_eqn

	mathml_eqn = unicodeNormalize(mathml_eqn)
	mathml_eqn = operatorNormalize(mathml_eqn)
	mathml_eqn = numberNormalize(mathml_eqn)
	return mathml_eqn

def generateIndex(NormalizedMathML):
	print "generateIndex invoked"
	input_file_unigrams_postinglist = open("../../Data/UnigramFeatures","r").read()
	input_file_bigrams_postinglist = open("../../Data/BigramFeatures","r").read()
	input_file_trigrams_postinglist = open("../../Data/TrigramFeatures","r").read()
	input_file_idf_scores = open("../../Data/IDF-Scores","r").read()

	unigrams_postinglist = ast.literal_eval(input_file_unigrams_postinglist)
	bigrams_postinglist = ast.literal_eval(input_file_bigrams_postinglist)
	trigrams_postinglist = ast.literal_eval(input_file_trigrams_postinglist)
	idf_scores = ast.literal_eval(input_file_idf_scores)

	unigrams = set()
	bigrams = set()
	trigrams = set()

	for x in unigrams_postinglist:
		unigrams.add(x)

	for x in bigrams_postinglist:
		bigrams.add(x)

	for x in trigrams_postinglist:
		trigrams.add(x)

	input_file = open(NormalizedMathML,"r")
	data = input_file.read()
	data = data.replace("\n"," ")
	lines = data.split('<m:math')
	mathML = []
	for line in lines :
		line = line.replace('\n', ' ')
		if len(line) == 0 :
			continue
		line = '<m:math' + line
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

	return (unigrams, bigrams, trigrams, idf_scores, unigrams_postinglist, bigrams_postinglist, trigrams_postinglist)

(unigrams, bigrams, trigrams, idf_scores, unigrams_postinglist, bigrams_postinglist, trigrams_postinglist) = generateIndex("../../Data/UnicodeNormalizedMathML.xml")