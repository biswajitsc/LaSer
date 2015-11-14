import sys
import re

sub = "\label{"

if __name__ == '__main__':

	cnt = 0
	outf = open('../../Data/FormulaeLabel', 'w')

	skip = set()
	with open('../../Data/error_line_by_line.txt','r') as f:
		for  line in f:
			ent = int(line.strip('\n'))
			# if ent  > 30000:
			# 	break
			skip.add(ent)

	cnt = 0
	cnt2 = 0
	with open('../../Data/Formulae', 'r') as f:
		for line in f:
			cnt += 1
			if cnt in skip:
				continue
			l = line.strip('\n')
			index = l.find(sub)
			if index != -1:
				index += 7
				label = ""
				while (l[index]!='}'):
					label += l[index]
					index += 1
				outf.write(str(cnt2)+' '+label+'\n')
			cnt2 += 1
	outf.close()