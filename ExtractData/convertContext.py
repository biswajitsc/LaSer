import sys

if __name__ == '__main__':
	skip = set()
	with open('../../Data/error_line_by_line.txt','r') as f:
		for  line in f:
			ent = int(line.strip('\n'))
			# if ent  > 30000:
			# 	break
			skip.add(ent-1)


	wf = open('../../Data/Context/eqncontext_2.txt','w')

	cnt = 0
	mapinds = {}
	for i in xrange(0,40000):
		if i not in skip:
			mapinds[i] = cnt
			cnt += 1



	with open('../../Data/Context/eqncontext.txt','r') as f:
		for line in f:
			temp = line.strip('\n').split(' ',1)
			if int(temp[0]) not in skip:
				wf.write(str(mapinds[int(temp[0])]) + ' ' + temp[1] + '\n')

	wf.close()			
