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

def genTreeStructure():

	global variations

	meta = open('../../Data/MathMLMeta.xml', 'r').readlines()
	mathXmlFile = open('../../Data/MathML.xml', 'r')
	cnt = -1
	for rawEquation in mathXmlFile:
		cnt += 1
		rawEq = rawEquation.strip('\n').replace('m:','')
		rawEq = rawEq.replace('xmlns', '')
		rawEq = rawEq.replace(':m', '')
		rawEq = rawEq.replace('="http://www.w3.org/1998/Math/MathML"','')
		# print rawEq
		try:
			variations = []
			# print rawEq
			genTreeStructureUtil(ET.fromstring(rawEq))
			print variations
			break
		except Exception as e:
			print e

	mathXmlFile.close()

def main():
	genTreeStructure()

if __name__ == '__main__':
	main()
