import sys
import re
import os
import codecs
import pickle

windowSize = 20

def parse(sentence):
	sentence = sentence.replace(',', ' ')
	tokens = sentence.split()
	res = {}
	isReference = [False for x in range(len(tokens))]
	idToEqns = {}
	for i in xrange(0, len(tokens)):
		m = re.findall('ref{([^}]*)',tokens[i])
		if m:
			#Extract all the equations being referred to
			idToEqns[i] = m[0]
			isReference[i] = True
			# print sentence.encode('ascii','ignore')

	for i in xrange(0, len(tokens)):
		if isReference[i]:
			before = ""
			for j in xrange(1, windowSize):
				if i - j < 0 or tokens[i - j].startswith('\\end'):
					break
				if not isReference[i - j]:
					before = tokens[i - j] + ' ' + before
			before = before[:-1]
			after = ""
			for j in xrange(1, windowSize):
				if i + j >= len(tokens) or tokens[i + j].startswith('\\begin'):
					break
				if not isReference[i + j]:
					after += tokens[i + j] + ' '
			after = after[:-1]

			if idToEqns in res.keys():	
				res[idToEqns[i]] = res[idToEqns[i]] + ' ' + before + ' ' + after
			else:
				res[idToEqns[i]] = before + ' ' + after
	return res

def main():
	skipped = 0
	cnt = 0
	#out = open('../../Data/Context/' + afile + '.pkl', 'wb')
	out = open('../../Data/Context/ref.txt', 'wb')
	
	labelsData = open('../../Data/FormulaeLabel').read().decode('cp1252', errors='ignore').split('\n')
	labels = {}

	for line in labelsData:
		try:
			labels[line.split(' ',1)[1]] = line.split(' ',1)[0]
		except:
			print line

	for year in reversed(xrange(1992, 2004)):

		print 'Processing year {0}'.format(year)
		files = os.listdir('../../Dataset/{0}'.format(year))
		for afile in files:
			cnt += 1
			if cnt % 100 == 0:
				print "Done ", cnt, "Skipped ", skipped

			try:
				data = open('../../Dataset/{0}/{1}'.format(year,afile), 'r').read().decode('cp1252', errors='ignore')
				lines = data.split('\n')
				data = ""
				for line in lines:
					if (line.startswith('%')):
						continue
					if re.match('\\\\def.*',line):
						continue
					data += ' ' + line

#				sentences = re.compile('\.\s+').split(data);
				
#				for sentence in sentences:
				res = parse(data)
				#pickle.dump(res,out)
				for key in res.keys():
					if key in labels.keys(): 
						print labels[key] + ' ' + ' ' + key + ' ' + res[key]


				out.close()

			except Exception as obj:
				print year, afile
				print obj
				raise
	

if __name__ == '__main__':
	main()