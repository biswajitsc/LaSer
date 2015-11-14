from lxml import etree
from StringIO import *
import re
import sys

import xml.etree.ElementTree as ET
import sys

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

# def genTreeStructure():

# 	global variations

# 	meta = open('../../Data/MathMLMeta.xml', 'r').readlines()
# 	mathXmlFile = open('../../Data/MathML.xml', 'r')
# 	cnt = -1
# 	for rawEquation in mathXmlFile:
# 		cnt += 1
# 		rawEq = rawEquation.strip('\n').replace('m:','')
# 		rawEq = rawEq.replace('xmlns', '')
# 		rawEq = rawEq.replace(':m', '')
# 		rawEq = rawEq.replace('="http://www.w3.org/1998/Math/MathML"','')
# 		# print rawEq
# 		try:
# 			variations = []
# 			# print rawEq
# 			genTreeStructureUtil(ET.fromstring(rawEq))
# 			print variations
# 			break
# 		except Exception as e:
# 			print e

# 	mathXmlFile.close()



def convertEquation(mathML) :

	global variations
	expressions = []
	j = 0
	for rawEquation in mathML :
		j += 1
		rawEq = rawEquation.strip('\n').replace('m:','')
		rawEq = rawEq.replace('xmlns', '')
		rawEq = rawEq.replace(':m', '')
		rawEq = rawEq.replace('="http://www.w3.org/1998/Math/MathML"','')
		# print rawEq
		try:
			variations = []
			# print rawEq
			genTreeStructureUtil(ET.fromstring(rawEq))
			# print variations
			newExp = ''
			for variation in variations:
				newExp += variation + ' '
			expressions.append(newExp)
		except Exception as e:
			print e

		
	return expressions


# def convertEquation(mathML) :
# 	expressions = []
# 	j = 0
# 	for eqn in mathML :
# 		j += 1
# 		try :
# 			string = eqn.replace(' xmlns="', ' xmlnamespace="')
# 			parser = etree.XMLParser(ns_clean=True,remove_pis=True,remove_comments=True)
# 			tree   = etree.parse(StringIO(string), parser)
# 			root = tree.getroot()
# 			tags = root.findall('.//')
# 			strng = ""
# 			for tag in tags :
# 				if tag.text == None or len(tag.text) == 0 :
# 					continue
# 				text = tag.text.strip()
# 				if len(text) != 0 :
# 					strng += text + " "
# 			expressions.append(strng)
# 		except Exception as ex :
# 			print j, ex, len(eqn.split(' '))
# 			continue
# 	print expressions
# 	return expressions
