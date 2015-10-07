import xml.etree.ElementTree as ET
# from bs4 import BeautifulSoup
import sys


def reduceExpression(terminalXml,depth):
	
	variations = []

	terminalXmlText = ''
	if terminalXml.text == None:
		terminalXmlText = ' '
	else:
		terminalXmlText = terminalXml.text

	if terminalXml.tag == 'mo':
		tempString = '<'+terminalXml.tag+'>'
		if terminalXml.text.strip() == '':
			tempString += ' * '
		else:
			tempString += ' ' + terminalXmlText + ' '
		tempString += '</'+terminalXml.tag+'>'
		variations.append(tempString)

	if terminalXml.tag == 'mi' or terminalXml.tag == 'mn':
		if depth < 0 and depth > -3:
			variations.append('<'+'mi'+'> '+'Expression'+' </'+'mi'+'>')
		variations.append('<'+terminalXml.tag+'> '+terminalXmlText+' </'+terminalXml.tag+'>')


	return variations,depth-1

def genTreeStructureUtil(rawXml,depth):
	if (len(list(rawXml))) <= 0:
		return reduceExpression(rawXml,0)

	variations = []
	variations.append('')	
	
	for child in rawXml:	
		tempa,depth2 = genTreeStructureUtil(child,depth)
		tempVariations = []
		for i in xrange(0,len(variations)):
			for j in xrange(0,len(tempa)):
				tempVariations.append(variations[i]+' '+tempa[j])
		variations = []		
		for i in xrange(0,len(tempVariations)):
			variations.append(tempVariations[i])

	for i in xrange(0,len(variations)):
		variations[i] = '<' + rawXml.tag + '> ' + variations[i] + ' </' + rawXml.tag + '>'

	if depth2 < 0 and depth2 > -3:
		variations.append('<mi> Expression </mi>')

	return variations,depth2-1
		
def genTreeStructure():
	meta = open('../../Data/MathMLMeta.xml', 'r').readlines()
	structureMathML = open('../../Data/StructureMathML.xml', 'w')
	structureMathMLMeta = open('../../Data/StructureMathMLMeta.xml', 'w')
	mathXmlFile = open('../../Data/MathML.xml', 'r')
	structToOrigMap = open('../../Data/StructureToOrig.xml', 'w')
	cnt = -1
	for rawEquation in mathXmlFile:
		cnt += 1
		rawEq = rawEquation.strip('\n').replace('m:','')
		rawEq = rawEq.replace('xmlns:m="http://www.w3.org/1998/Math/MathML"','')
		print rawEq
		try:
			variations,depth = genTreeStructureUtil(ET.fromstring(rawEq),100000)
			variations = variations[:-1]
			for variation in variations:
				structureMathML.write(variation.encode('utf-8') + '\n')
				structureMathMLMeta.write(meta[cnt].strip('\n')+'\n')
				structToOrigMap.write(str(cnt)+'\n')
		except Exception as e:
			print e
		if cnt >= 0:
			break
	
	structureMathML.close()
	structureMathMLMeta.close()
	structToOrigMap.close()
	mathXmlFile.close()

def main():
	genTreeStructure()

if __name__ == '__main__':
	main()
