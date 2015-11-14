import sys
import re
import os
import codecs
import pickle
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

windowSize = 10
	
def filterText(inp):
	inp = re.sub('\W+',' ',inp)
	clean_inp = ""
	inp_words = inp.split()
	for word in inp_words:
		if word not in stop and len(word) >= 3:
			clean_inp += word + ' '
	clean_inp = clean_inp.strip()
	return clean_inp
	return inp

def parse(data,eqn):
	# for i in keymaps.keys():
	# 	sentence = sentence.replace(keymaps[i],i)
	# sentence = sentence.replace(',', ' ')
	#print eqn
	#print data
	data = data.replace(eqn,' SETSUNA_DAISUKI ')
	eqn = 'SETSUNA_DAISUKI'
	# ind = data.find(eqn)
	tokens = data.split()
	res = {}
	ids = []

	print 'here parse'

	for i in xrange(0, len(tokens)):
		if tokens[i] == eqn:
			ids.append(i)
	print len(ids)
	for i in ids:
		# if i%1000 == 0:
		# 	print i,len(tokens)
		# while ptr < len(ids) and i < ids[ptr]:
		# 	ptr += 1
		# if ptr == len(ids):
		# 	break
		if True:
			if i % 1000 == 0:
				print i
			before = ""
			for j in xrange(1, windowSize):
				if i - j < 0 or tokens[i - j].startswith('\\end'):
					break
				if len(before) > 0:
					before += ' '
				before += tokens[i - j]
			after = ""
			for j in xrange(1, windowSize):
				if i + j >= len(tokens) or tokens[i + j].startswith('\\begin'):
					break
				after += tokens[i + j] + ' '
			after = after[:-1]
			before = before[::-1]
			if eqn in res.keys():	
				res[eqn] = res[eqn] + ' ' + before + ' ' + after
			else:
				res[eqn] = before + ' ' + after

	# print 'return res'

	return res

def main():
	meta = open('../../Data/MathMLMeta.xml').read().decode('cp1252', errors='ignore').split('\n')
	equations = open('../../Data/MathML.xml').read().decode('cp1252', errors='ignore').split('\n')

	skipped = 0
	cnt = 0
	out = codecs.open('../../Data/Context/eqncontext.txt', 'w', 'cp1252')

	for i in xrange(0, len(meta)):
		print cnt
		doc = meta[i]
		eqn = equations[i]
		# cnt += 1
		if cnt % 100 == 0:
			print "Done ", cnt, "Skipped ", skipped
		try:
			# print '1'
			data = open('../../Dataset/{0}/{1}'.format(doc.split(' ')[0],doc.split(' ')[1]), 'r').read().decode('cp1252', errors='ignore')
			data = data.replace('\n','  ')
			# print '2'
			res = parse(data,eqn)
			if 'SETSUNA_DAISUKI' not in res.keys():
				skipped += 1
				continue
			print '3'
			out.write(str(i) + ' ' + filterText(res['SETSUNA_DAISUKI']) + '\n')
			out.flush()
						
		except Exception as obj:
			print doc
			print obj

	out.close()

if __name__ == '__main__':
	main()