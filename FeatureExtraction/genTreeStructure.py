import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys


def reduceExpression(terminalXml):
	
	variations = []


	if terminalXml.tag == 'mo':
		tempString = '<'+terminalXml.tag+'>'
		if terminalXml.text.strip() == '':
			tempString += '*'
		else:
			tempString += terminalXml.text
		tempString = '</'+terminalXml.tag+'>'
		variations.append(tempString)

	if terminalXml.tag == 'mi' or terminalXml.tag == 'mn':
		variations.append('<'+'mi'+'>'+'Variable'+'</'+'mi'+'>')
		variations.append('<'+terminalXml.tag+'>'+terminalXml.text+'</'+terminalXml.tag+'>')

	return variations

def genTreeStructureUtil(rawXml):
	if (len(list(rawXml))) <= 0:
		return reduceExpression(rawXml)

	variations = []
	variations.append('')	
	
	for child in rawXml:	
		tempa = genTreeStructureUtil(child)
		tempVariations = []
		for i in xrange(0,len(variations)):
			for j in xrange(0,len(tempa)):
				tempVariations.append(variations[i]+' '+tempa[j])
		variations = []		
		for i in xrange(0,len(tempVariations)):
			variations.append(tempVariations[i])

	for i in xrange(0,len(variations)):
		variations[i] = '<' + rawXml.tag + '>' + variations[i] + '</' + rawXml.tag + '>'

	variations.append('</Expression>')

	return variations
		
def genTreeStructure(mathmlXml,mathmlMeta):
	meta = open(mathmlMeta, 'r').readlines()
	structureMathML = open('../../Data/StructureMathML.xml', 'w')
	structureMathMLMeta = open('../../Data/StructureMathMLMeta.xml', 'w')
	tree = ET.parse(mathmlXml)
	rawEquations = tree.getroot()
	cnt = -1
	for rawEquation in rawEquations.findall('math'):
		cnt += 1
		variations = genTreeStructureUtil(rawEquation)
		for variation in variations:
			structureMathML.write(str(cnt+1) + ' ' + variation.encode('utf-8') + '\n')
			structureMathMLMeta.write(meta[cnt].strip('\n')+'\n')
	
	structureMathML.close()
	structureMathMLMeta.close()

def main():
	genTreeStructure('../../Data/MathML.xml','../../Data/MathMLMeta.xml')
	

if __name__ == '__main__':
	main()