import os
import sys
import re

def main():
	formulae = open(sys.argv[1], 'r')
	mathMLOutput = open(sys.argv[2], 'w')
	tempFile = '../../Data/tmp.txt'
	errorFile = open('../../Data/error.txt', 'w')
	mathMLOutput.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
	
	cnt = 0
	for eqn in formulae:
		cnt += 1
		cleanEqn = eqn.strip('\n').strip()
		cleanEqn = re.sub('\\\\','\\\\\\\\',cleanEqn)
		cleanEqn = re.sub('\)','\\\\)',cleanEqn)
		cleanEqn = re.sub('\(','\\\\(',cleanEqn)
		# print cleanEqn
		oscommand = 'latexmlmath --pmml=- ' + cleanEqn + ' > ' + tempFile
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
			mathmlOutTemp.close()
			os.remove(tempFile)
		except Exception as e:
			errorFile.write( str(cnt) + '\n' )
			
		if cnt % 10000 == 0:
			print cnt
	
	formulae.close()
	mathMLOutput.close()
	errorFile.close()	

if __name__ == '__main__':
	main()