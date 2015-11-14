import sys

if __name__ == '__main__':

	context = {}
	with open('../../Data/Context/eqncontext_2.txt','r') as f:
		for line in f:
			temp = line.strip('\n').split(' ',1)
			index = int(temp[0])
			if index not in context.keys():
				context[index] = ''
			context[index] += temp[1]

	with open('../../Data/Context/ref.txt','r') as f:
		for line in f:
			temp = line.strip('\n').split(' ',1)
			index = int(temp[0])
			if index not in context.keys():
				context[index] = ''
			context[index] += temp[1]

	cnt = 0
	with open('../../Data/Context/equation_context.txt','w') as f:
		for i in xrange(0,10000):
			if i not in context.keys():
				f.write('\n')
				cnt += 1
			else:
				f.write(context[i] + '\n')

	print cnt			



