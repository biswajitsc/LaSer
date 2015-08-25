import os
import sys
import re

def main():
	formulae = open('../../Data/Formulae', 'r')
	meta = open('../../Data/Meta', 'r').readlines()
	mathMLOutput = open('../../Data/MathML.xml', 'w')
	metaOutput = open('../../Data/MathMLMeta.xml', 'w')
	tempFile = '../../Data/tmp.txt'
	errorFile = open('../../Data/error.txt', 'w')
	# mathMLOutput.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')

	
	cnt = -1
	for eqn in formulae:
		cnt += 1
		cleanEqn = eqn.strip('\n').strip()
		# cleanEqn = re.sub('\\\\','\\\\\\\\',cleanEqn)
		# cleanEqn = re.sub('\)','\\\\)',cleanEqn)
		# cleanEqn = re.sub('\(','\\\\(',cleanEqn)
		# print cleanEqn

		oscommand = "latexmlmath --pmml=- \"" + cleanEqn + "\" > " + tempFile
		# print oscommand
		os.system(oscommand)
		
		try:
			mathmlOutTemp = open(tempFile,'r')
			tempString = ''
			linecnt = 0
			for line in mathmlOutTemp:
			 	if linecnt > 0:
			 		tempString += line.strip('\n') + ' '
			 	linecnt += 1
			mathMLOutput.write(tempString+'\n')
			metaOutput.write(meta[cnt])
			mathmlOutTemp.close()
			os.remove(tempFile)
		except Exception as e:
			errorFile.write( str(cnt) + '\n' )
		

		if cnt % 10000 == 0:
			print cnt

	
	formulae.close()
	mathMLOutput.close()
	errorFile.close()	
	metaOutput.close()

if __name__ == '__main__':
	main()