import os
import re
import sys
import math
import web
import json
import urllib
import operator
from HelperFunctions import *


# render_xml = lambda message: '<message>%s</message>'%message
# render_html = lambda message: '<html><body>%s</body></html>'%message
# render_txt = lambda message: message

urls = (
	'/(.*)', 'greet'
)

app = web.application(urls, globals())

val = 0

def generateRankedListBasedOnContext(query):

	global context_unigrams
	global context_bigrams
	global context_trigrams
	global context_idf_scores
	global context_unigrams_postinglist
	global context_bigrams_postinglist
	global context_trigrams_postinglist
	global original_metadata
	global original_eqns


	query = re.sub('\W',' ',query)
	context_query = urllib.unquote(query).decode('utf8')

	query_vector = extractContextWeights(context_query, context_idf_scores, context_unigrams, context_bigrams, context_trigrams)

	matched_eqns = set()
	cosine_similarities = {}

	for feature in query_vector:
		if feature in context_unigrams:
			for eqn_id, frequency in context_unigrams_postinglist[feature]:
				if eqn_id not in cosine_similarities:
					cosine_similarities[eqn_id] = 0.0
					matched_eqns.add(eqn_id)
				cosine_similarities[eqn_id] += (context_idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature]
		elif feature in context_bigrams:
			for eqn_id, frequency in context_bigrams_postinglist[feature]:
				if eqn_id not in cosine_similarities:
					cosine_similarities[eqn_id] = 0.0
					matched_eqns.add(eqn_id)
				cosine_similarities[eqn_id] += (context_idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature]
		elif feature in context_trigrams:
			for eqn_id, frequency in context_trigrams_postinglist[feature]:
				if eqn_id not in cosine_similarities:
					cosine_similarities[eqn_id] = 0.0
					matched_eqns.add(eqn_id)
				cosine_similarities[eqn_id] += (context_idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature]
		# else:
		# 	print "This should not have bloody fucking happened"

	mod_weight = {}
	eqns = set()
	print matched_eqns

	for eqn_id in matched_eqns:
		eqns.add(eqn_id)
		mod_weight[eqn_id] = 0.0

	for feature in context_unigrams_postinglist:
		for eqn_id, frequency in context_unigrams_postinglist[feature]:
			if eqn_id in eqns:
				mod_weight[eqn_id] += (context_idf_scores[feature]*(1+math.log(frequency)))*(context_idf_scores[feature]*(1+math.log(frequency)))

	for feature in context_bigrams_postinglist:
		for eqn_id, frequency in context_bigrams_postinglist[feature]:
			if eqn_id in eqns:
				mod_weight[eqn_id] += (context_idf_scores[feature]*(1+math.log(frequency)))*(context_idf_scores[feature]*(1+math.log(frequency)))

	for feature in context_trigrams_postinglist:
		for eqn_id, frequency in context_trigrams_postinglist[feature]:
			if eqn_id in eqns:
				mod_weight[eqn_id] += (context_idf_scores[feature]*(1+math.log(frequency)))*(context_idf_scores[feature]*(1+math.log(frequency)))

	for eqn_id in eqns:
		mod_weight[eqn_id] = math.sqrt(mod_weight[eqn_id])

	for eqn_id in cosine_similarities:
		cosine_similarities[eqn_id] = cosine_similarities[eqn_id]/mod_weight[eqn_id]

	#tupple of eqn_id , score
	sorted_cosine_similarities_list = []

	for eqn_id, score in cosine_similarities.items():
		sorted_cosine_similarities_list.append((eqn_id, score))

	sorted_cosine_similarities_list = sorted(sorted_cosine_similarities_list, key=lambda tup: tup[1], reverse=True)

	ranked_list = {}
	ranked_eqns = set()
	i = 0

	for eqn_id, score in sorted_cosine_similarities_list:
		if eqn_id not in ranked_eqns:
			i += 1
			ranked_eqns.add(eqn_id)
			doc_id = original_metadata[int(eqn_id)-1].split(" ")[1]
			print eqn_id
			eqn = original_eqns[eqn_id-1]
			tempDict = {}
			tempDict['original_doc_id'] = doc_id
			
			eqn = unicode(eqn, "utf-8")

			eqn = eqn.encode('ascii', 'xmlcharrefreplace')                    
			tempDict['original_eqn'] = eqn
			tempDict['doc_id'] = eqn_id
			tempDict['score'] = score
			# ranked_list.append((doc_id,score,int(original_doc_id),original_eqn))
			ranked_list[i] = tempDict
		if i == 50:
			break

	return ranked_list

def generateRankedListBasedOnEquation(query):

	global unigrams
	global bigrams
	global trigrams
	global idf_scores
	global unigrams_postinglist
	global bigrams_postinglist
	global trigrams_postinglist
	global metadata
	global original_eqns

	latex_eqn = urllib.unquote(query).decode('utf8')


	# print "#############"
	# print "in generateRankedLists : latex_eqn is ",latex_eqn
	# print "#############"

	mathML_eqn = generateMathML(latex_eqn)

	# print "#############"
	# print "in generateRankedLists : mathML_eqn is ",mathML_eqn
	# print "#############"


	# work with both the simplified eqn as well as the original eqn

	mathML_eqns = normalizeQuery(mathML_eqn)
	# print "Eqns :",len(mathML_eqns)

	simplified_mathML_eqn = simplifyMathML(mathML_eqn)	
	# simplified_mathML_eqns = normalizeQuery(simplified_mathML_eqn)
	simplified_mathML_eqns = []

	# print "#############"
	# print "in generateRankedLists : number normalized mathml is ",mathML_eqn
	# print "#############"

	# print "#############"
	# print "in generateRankedLists : unicode normalized mathml is ",mathML_eqn
	# print "#############"



	query_vectors = []
	simplified_query_vectors = []

	for eqn in mathML_eqns:
		query_vectors.append(extractWeights(eqn, idf_scores, unigrams, bigrams, trigrams))

	for eqn in simplified_mathML_eqns:
		simplified_query_vectors.append(extractWeights(eqn, idf_scores, unigrams, bigrams, trigrams))


	# Matching

	# Determine the matching docs

	# list of sets
	matched_docs_list = []
	simplified_matched_docs_list = []

	# list of dictionaries
	cosine_similarities = []
	simplified_cosine_similarities = []


	#print "features in query are"
	#print query_vectors
	#print simplified_query_vectors

	fuck = set()

	for x in range(len(query_vectors)):
		query_vector = query_vectors[x]
		cosine_similarity = {}
		matched_docs = set()
		for feature in query_vector:
			# identify the type of feature
			print "Feature : ", feature
			if feature in unigrams:
				for doc_id, frequency in unigrams_postinglist[feature]:
					if doc_id not in cosine_similarity:
						cosine_similarity[doc_id] = 0.0
						matched_docs.add(doc_id)
					cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] #- idf_scores[feature]*query_vector[feature]fuck.add(feature)
					fuck.add(feature)

			elif feature in bigrams:
				for doc_id, frequency in bigrams_postinglist[feature]:
					if doc_id not in cosine_similarity:
						cosine_similarity[doc_id] = 0.0
						matched_docs.add(doc_id)
					cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] #- idf_scores[feature]*query_vector[feature]
					fuck.add(feature)

			elif feature in trigrams:
				for doc_id, frequency in trigrams_postinglist[feature]:
					if doc_id not in cosine_similarity:
						cosine_similarity[doc_id] = 0.0
						matched_docs.add(doc_id)
					cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*query_vector[feature] #- idf_scores[feature]*query_vector[feature]
					fuck.add(feature)
			# else:
			# 	print "This should not have happened for feature ", feature
		cosine_similarities.append(cosine_similarity)
		matched_docs_list.append(matched_docs)

	for x in range(len(simplified_query_vectors)):
		simplified_query_vector = simplified_query_vectors[x]
		simplified_cosine_similarity = {}
		simplified_matched_docs = set()
		for feature in simplified_query_vector:
			# identify the type of feature
			if feature in unigrams:
				for doc_id, frequency in unigrams_postinglist[feature]:
					if doc_id not in simplified_cosine_similarity:
						simplified_cosine_similarity[doc_id] = 0.0
						simplified_matched_docs.add(doc_id)
					simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] #- idf_scores[feature]*simplified_query_vector[feature]
					fuck.add(feature)

			elif feature in bigrams:
				for doc_id, frequency in bigrams_postinglist[feature]:
					if doc_id not in simplified_cosine_similarity:
						simplified_cosine_similarity[doc_id] = 0.0
						simplified_matched_docs.add(doc_id)
					simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] #- idf_scores[feature]*simplified_query_vector[feature]
					fuck.add(feature)

			elif feature in trigrams:
				for doc_id, frequency in trigrams_postinglist[feature]:
					if doc_id not in simplified_cosine_similarity:
						simplified_cosine_similarity[doc_id] = 0.0
						simplified_matched_docs.add(doc_id)
					simplified_cosine_similarity[doc_id] += (idf_scores[feature] * (1 + math.log(frequency)))*simplified_query_vector[feature] #- idf_scores[feature]*simplified_query_vector[feature]
					fuck.add(feature)
			# else:
				# print "This should not have happened"
		simplified_cosine_similarities.append(simplified_cosine_similarity)
		simplified_matched_docs_list.append(simplified_matched_docs)

		# print 'fucked: ',fuck

	# for x in range(len(query_vectors)):
	# 	query_vector = query_vectors[x]
	# 	matched_docs = matched_docs_list[x]
	# 	for feature in query_vector:
	# 		for doc_id in matched_docs:
	# 			cosine_similarities[x][doc_id] += idf_scores[feature]*query_vector[feature]

	# for x in range(len(simplified_query_vectors)):
	# 	simplified_query_vector = simplified_query_vectors[x]
	# 	simplified_matched_docs = simplified_matched_docs_list[x]
	# 	for feature in simplified_query_vector:
	# 		for doc_id in simplified_matched_docs:
	# 			simplified_cosine_similarities[x][doc_id] += idf_scores[feature]*simplified_query_vector[feature]

	# we have the numerators
	# traverse the entire postings list to compute the denominator

	# Matching docs computed

	# determine the cosine similarity with each matched doc

	# set denoting the docs to be considered
	docs = set()
	mod_weight = {}

	for doc_ids in matched_docs_list:
		for doc_id in doc_ids:
			docs.add(doc_id)

	for doc_ids in simplified_matched_docs_list:
		for doc_id in doc_ids:
			docs.add(doc_id);

	for doc_id in docs:
		mod_weight[doc_id] = 0.0

	for feature in unigrams_postinglist:
		for doc_id, frequency in unigrams_postinglist[feature]:
			if doc_id in docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))


	for feature in bigrams_postinglist:
		for doc_id, frequency in bigrams_postinglist[feature]:
			if doc_id in docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))

	for feature in trigrams_postinglist:
		for doc_id, frequency in trigrams_postinglist[feature]:
			if doc_id in docs:
				mod_weight[doc_id] += (idf_scores[feature]*(1+math.log(frequency)))*(idf_scores[feature]*(1+math.log(frequency)))

	for doc_id in docs:
		mod_weight[doc_id] = math.sqrt(mod_weight[doc_id])

	for x in range(len(cosine_similarities)):
		for doc_id in cosine_similarities[x]:
			cosine_similarities[x][doc_id] = cosine_similarities[x][doc_id]/mod_weight[doc_id]


	for x in range(len(simplified_cosine_similarities)):
		for doc_id in simplified_cosine_similarities[x]:
			simplified_cosine_similarities[x][doc_id] = simplified_cosine_similarities[x][doc_id]/mod_weight[doc_id]

	# sort the cosine similarity vales corresponding to each query variant and store in a list

	sorted_cosine_similarities_list = []
	
	for x in range(len(cosine_similarities)):
		for doc_id, score in cosine_similarities[x].items():
			sorted_cosine_similarities_list.append((doc_id,score))
	
	for x in range(len(simplified_cosine_similarities)):
		for doc_id, score in simplified_cosine_similarities[x].items():
			sorted_cosine_similarities_list.append((doc_id,score))

	sorted_cosine_similarities_list = sorted(sorted_cosine_similarities_list, key=lambda tup: tup[1], reverse=True)
	# print sorted_cosine_similarities_list
	# get the best score corresponding to each doc

	ranked_list = {}
	ranked_docs = set()

	# Limit the returned results to 50

	i=0

	for doc_id, score in sorted_cosine_similarities_list:
		if doc_id not in ranked_docs:
			i += 1
			ranked_docs.add(doc_id)
			# print int(doc_id), len(metadata), " Metadata"
			original_doc_id = metadata[int(doc_id)-1]
			original_eqn = original_eqns[int(original_doc_id.split(" ")[2]) - 1]
			tempDict = {}
			tempDict['doc_id'] = original_doc_id.split(" ")[2].strip('\n')
			original_doc_id = original_doc_id.split(" ")[1]
			tempDict['original_doc_id'] = original_doc_id
			
			original_eqn = unicode(original_eqn, "utf-8")

			original_eqn = original_eqn.encode('ascii', 'xmlcharrefreplace')                    
			tempDict['original_eqn'] = original_eqn
			tempDict['score'] = score
			# print tempDict
			# ranked_list.append((doc_id,score,int(original_doc_id),original_eqn))
			ranked_list[i] = tempDict
		if i == 50:
			break
	return ranked_list


def generateRankedList(context_ans,equation_ans):

	ans_list2 = {}
	i = 0
	for key,item in equation_ans.items():
		ans_list2[item['doc_id']] = (item['original_doc_id'],item['original_eqn'],0.7*item['score'],item['doc_id'])
		i += 1
	
	for key,item in context_ans.items():
		if item['doc_id'] in ans_list2.keys():
			score = ans_list2[item['doc_id']][2] + 0.3*item['score']
			print item['original_eqn']
			print ans_list2[item['doc_id']][2], item['score']
			ans_list2[item['doc_id']] = (item['original_doc_id'],item['original_eqn'],score,item['doc_id'])
		else:
			ans_list2[item['doc_id']] = (item['original_doc_id'],item['original_eqn'],0.3*item['score'],item['doc_id'])
		i += 1
	
	ans_list3 = []
	for key,val in ans_list2.items():
		ans_list3.append(val)

	ans_list = sorted(ans_list3, key=lambda tup: tup[2], reverse=True)

	ans = {}
	for i in xrange(0,len(ans_list)):
		tempDict = {}
		tempDict['original_doc_id'] = ans_list[i][0]
		tempDict['original_eqn'] = ans_list[i][1]
		tempDict['score'] = ans_list[i][2]
		tempDict['doc_id'] = ans_list[i][3]
		print tempDict['doc_id']
		ans[i] = tempDict

	return ans

class greet:

	def GET(self, query):
	#split the query into equation and context part
		context_ans = {}
		equation_ans = {}
		context_query = query.split('$$$')[1].lower()
		equation_query = query.split('$$$')[0]
		if len(context_query.strip())>0:
			context_ans = generateRankedListBasedOnContext(context_query)
		else:
			print "no context query"
			context_ans = {}
		if len(equation_query.strip()) > 0:
			equation_ans = generateRankedListBasedOnEquation(equation_query)
		else:
			print "no equation_query"
			equation_ans = {}
		latex_formulae = []
		#latex_fddormulae.append("a = b")
		#latex_formulae.append("b = c")
		archive_id = []
		#archive_id.append("1")
		#archive_id.append("2")
		archive_links = []
		#archive_links.append('https//papers.com/1')
		#archive_links.append('https//papers.com/2')
		web.header('Content-Type', 'application/json')
		#print ans
		# return str(ans).decode('utf-8')
		ans = generateRankedList(context_ans,equation_ans)
		if context_query or equation_query:
			return json.dumps(ans,ensure_ascii=False)#, 'latex_formulae' : latex_formulae, 'archive_id' : archive_id, 'archive_links' : archive_links}

	def PUT(self,value):
		val = value
		print "PUT",val

if __name__ == "__main__":
	app.run()
