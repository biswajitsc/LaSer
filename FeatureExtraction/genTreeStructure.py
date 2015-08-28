import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys


def reduceExpression(terminalXml):
	
	variations = []

	terminalXmlText = ''
	if terminalXml.text == None:
		terminalXmlText = ' '
	else:
		terminalXmlText = terminalXml.text

	if terminalXml.tag == 'mo':
		tempString = '<'+terminalXml.tag+'>'
		if terminalXml.text.strip() == '':
			tempString += '*'
		else:
			tempString += terminalXmlText
		tempString = '</'+terminalXml.tag+'>'
		variations.append(tempString)

	if terminalXml.tag == 'mi' or terminalXml.tag == 'mn':
		variations.append('<'+'mi'+'> '+'Variable'+' </'+'mi'+'>')
		variations.append('<'+terminalXml.tag+'> '+terminalXmlText+' </'+terminalXml.tag+'>')

	variations.append(' </Expression> ')

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
		variations[i] = '<' + rawXml.tag + '> ' + variations[i] + ' </' + rawXml.tag + '>'

	variations.append(' </Expression> ')

	return variations
		
def genTreeStructure(mathmlXml,mathmlMeta):
	meta = open(mathmlMeta, 'r').readlines()
	structureMathML = open('../../Data/StructureMathML.xml', 'w')
	structureMathMLMeta = open('../../Data/StructureMathMLMeta.xml', 'w')
	
	mathXmlFile = open(mathmlXml, 'r')
	cnt = -1
	for rawEquation in mathXmlFile:
		cnt += 1
		print rawEquation.replace('m:','')
		variations = genTreeStructureUtil(ET.fromstring(rawEquation.replace('m:','')))
		for variation in variations:
			structureMathML.write(str(cnt+1) + ' ' + variation.encode('utf-8') + '\n')
			structureMathMLMeta.write(meta[cnt].strip('\n')+'\n')

		if cnt >= 0:
			break
	
	structureMathML.close()
	structureMathMLMeta.close()
	mathXmlFile.close()

def main():
	genTreeStructure('../../Data/MathML.xml','../../Data/MathMLMeta.xml')
	

if __name__ == '__main__':
	main()