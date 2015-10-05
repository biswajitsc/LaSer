import sys
import re
import os
import codecs
import pickle

windowSize = 10

def parse(sentence):
	sentence = sentence.replace(',', ' ')
	tokens = sentence.split()
	res = []
	isSymbol = [False for x in range(len(tokens))]
	idToEqns = {}
	for i in xrange(0, len(tokens)):
		m = re.findall('ref{eq:([^}]*)',tokens[i])
		if m:
			#Extract all the equations being referred to
			idToEqns[i] = m
			isSymbol[i] = True
			# print sentence.encode('ascii','ignore')

	for i in xrange(0, len(tokens)):
		if isSymbol[i]:
			before = ""
			for j in xrange(1, windowSize):
				if i - j < 0 or tokens[i - j].startswith('\\end'):
					break
				if not isSymbol[i - j]:
					before = tokens[i - j] + ' ' + before
			before = before[:-1]
			after = ""
			for j in xrange(1, windowSize):
				if i + j >= len(tokens) or tokens[i + j].startswith('\\begin'):
					break
				if not isSymbol[i + j]:
					after += tokens[i + j] + ' '
			after = after[:-1]
			res.append((before, idToEqns[i], after))
	return res

def main():
	skipped = 0
	cnt = 0

	for year in reversed(xrange(1992, 2004)):

		print 'Processing year {0}'.format(year)
		files = os.listdir('../../Dataset/{0}'.format(year))
		for afile in files:
			cnt += 1
			out = open('../../Data/Context/' + afile + '.pkl', 'wb')
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

				sentences = re.compile('\.\s+').split(data);
				
				for sentence in sentences:
					res = parse(sentence)
			        pickle.dump(res,out)
					
				out.close()

			except Exception as obj:
				print year, afile
				print obj
				raise
	

if __name__ == '__main__':
	main()