import os
import sys
import re
import subprocess

def main():
	formulae = open('../../Data/Formulae', 'r')
	meta = open('../../Data/Meta', 'r').readlines()
	mathMLOutput = open('../../Data/MathML.xml', 'w')
	metaOutput = open('../../Data/MathMLMeta.xml', 'w')
	tempFile = '../../Data/tmp.txt'
	errorFile = open('../../Data/error.txt', 'w')
	# mathMLOutput.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')

	
	cnt = 0
	skipped = 0

	stars = "*********************************************"

	for eqn in formulae:
		cnt += 1
		cleanEqn = eqn.strip('\n').strip()
		cleanEqn = re.sub('"','',cleanEqn)
		# print cleanEqn
		# cleanEqn = re.sub('\\\\','\\\\\\\\',cleanEqn)
		# cleanEqn = re.sub('\)','\\\\)',cleanEqn)
		# cleanEqn = re.sub('\(','\\\\(',cleanEqn)
		# print cleanEqn

		oscommand = "latexmlmath --pmml=- \"" + cleanEqn + "\" > " + tempFile
		print stars
		print oscommand
		print stars

		# os.system(oscommand)
		try:
			result = subprocess.check_output(oscommand, stderr=subprocess.STDOUT, shell=True)
		except Exception as e:
			result = str(e)
		
		try:
			if len(result) > 0:
				print "Cannot parse eqn"
				raise Exception("Cannot parse eqn")

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
			errorFile.write( stars + '\n' + str(cnt) + '\n' + result + '\n' + stars + '\n')
			skipped += 1
		

		print "Done ", cnt, "Skipped ", skipped


		mathMLOutput.flush()
		metaOutput.flush()
		errorFile.flush()


	
	formulae.close()
	mathMLOutput.close()
	errorFile.close()	
	metaOutput.close()

if __name__ == '__main__':
	main()
