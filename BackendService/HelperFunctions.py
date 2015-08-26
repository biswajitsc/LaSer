# coding: utf-8

from lxml import etree
from StringIO import *
from lxml import objectify
import sympy
import re
import decimal
import unicodedata as ucode
import sys

def generateMathML(latex_eqn) :
    cleanEqn = eqn.strip('\n').strip()
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
	normalized = ''
	tokens = mathml_eqn.split()
	normalizedString = ""
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
	        print token
	return normalizedString

def extractWeights(mathml_eqn, idf_scores, unigrams, bigrams, trigrams) :
	mathml_eqn = mathml_eqn.replace('\n', ' ')
	mathml_eqn = mathml_eqn.replace('<?xml version="1.0"?>', '')
	mathml_eqn = re.sub(' +',' ',mathml_eqn)
	mathml_eqn = mathml_eqn.replace('\t', ' ')

	weight_score = {}
	
	for unigram in unigrams :
		string = str(unigram)
		if string in mathml_eqn :
			weight_score[unigram] = ((1 + math.log(mathml_eqn.count(string))) * idf_scores[unigram])
	for bigram in bigrams :
		string = (str(bigram[0]) + ' ' + str(bigram[1]))
		if string in mathml_eqn :
			weight_score[bigram] = ((1 + math.log(mathml_eqn.count(string))) * idf_scores[bigram])
	
	for trigram in trigrams :
		string = (str(trigram[0]) + ' ' + str(trigram[1]) + ' ' + str(trigram[2]))
		if string in mathml_eqn :
			weight_score[trigram] = ((1 + math.log(mathml_eqn.count(string))) * idf_scores[trigram])

	return weight_score

def normalizeQuery(mathml_eqn) :
	# simplifiedMathML = simplifyMathML(mathml_eqn)
	# if simplifiedMathML = "" :
	# 	simplifiedMathML = mathml_eqn
	mathml_eqn = numberNormalize(mathml_eqn)
	mathml_eqn = unicodeNormalize(mathml_eqn)
	return mathml_eqn

def generateIndex(NumberNormalizedMathML):
    input_file = open(NumberNormalizedMathML,"r")
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

    #for unigram in unigrams :
    #        output_file_unigrams.write("{" + str(unigram) + " : " + str(unigrams_postinglist[unigram]) + "}" + '\n')
    #for bigram in bigrams :
    #        output_file_bigrams.write("{" + str(bigram) + " : " + str(bigrams_postinglist[bigram]) + "}" + '\n')
    #for trigram in trigrams :
    #        output_file_trigrams.write("{" + str(trigram) + " : " + str(trigrams_postinglist[trigram]) + "}" + '\n')
    for features in feature_numDocs :
    #        output_file_idfs.write(str(features) + " : " + str(1 + math.log(numDocs/feature_numDocs[features])) + '\n')
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

    return unigrams, bigrams, trigrams, feature_numDocs, unigrams_postinglist, bigrams_postinglist, trigrams_postinglist, weight_matrix