import sys
import re

sub = "\label{"

if __name__ == '__main__':

	cnt = 0
	outf = open('../../Data/Formulae', 'w')
	with open('../../Data/FormulaeLabel', 'r') as f:
		for line in f:
			l = line.strip('\n')
			index = l.find(sub)
			if index != -1:
				index += 7
				label = ""
				while (l[index]!='}'):
					label += l[index]
					index += 1
				outf.write(str(cnt)+' '+label+'\n')
			cnt += 1
	outf.close()